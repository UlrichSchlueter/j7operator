from enum import Enum, auto
import jsons
import time
import random
import datetime
import logging
import yaml

from flask_executor import Executor

from ActionAdmin import ActionAdmin
from ActionAdmin import Action
from ActionAdmin import ActionState
from ActionAdmin import ActionType

from TaskAdmin import TaskAdmin
from TaskAdmin import Task
from TaskAdmin import TaskType
from TaskAdmin import TaskState
from JobAdmin import JobAdmin
from JobAdmin import Job
from JobAdmin import JobType
from JobAdmin import JobState


from AtomicCounter import AtomicCounter
from MnrHelper import MNRHelper
from RebootHelper import RebootHelper

logger = logging.getLogger('j7')
logger.warning("Administrator starting")

class Stats:
    def __init__(self):
        self.queuedActions=0
        self.activeActions=0
        self.failedActions=0
        self.finishedActions=0
        self.activeTasks=0
        self.failedTasks=0
        self.finishedTasks=0
        self.activeJobs=0
        self.failedJobs=0
        self.finishedJobs=0
        self.adminState=None
    

class AdministratorState(Enum):
    ACTIONS = auto()
    TASKS = auto()
    JOBS = auto()
    JOBS_TO_RUN = auto()
    PAUSED = auto()
    INIT= auto()

class Administrator:
    

    def __init__(self, app,executor, tasksAdmin,jobAdmin, actionAdmin):    
        self.app=app
        self.adminState=AdministratorState.INIT
        self.adminPhase=0
        self.executor=executor
        self.tasksAdmin=tasksAdmin
        self.actionAdmin=actionAdmin
        self.jobAdmin=jobAdmin
        self.actionCounter= AtomicCounter()        
        self.jobCounter= AtomicCounter()
        self.lastUpdate=time.time()
        self.readInventory("farm1")
        

    def setState(self,new_admin_state):
        self.adminState=new_admin_state
        self.lastUpdate=time.time()
        logger.warning("Switching to Adminstrator.state: " +str(self.adminState))
        if self.adminState==AdministratorState.ACTIONS:
            self.adminPhase=1
        elif self.adminState==AdministratorState.TASKS:
            self.adminPhase=2
        elif self.adminState==AdministratorState.JOBS_TO_RUN:
            self.adminPhase=3
        elif self.adminState==AdministratorState.JOBS:
            self.adminPhase=4

    def readInventory(self,name):
        filename="inventory/"+name+".yaml"
        with self.app.open_resource(filename) as f:
            mydata = yaml.load(f)
            print (mydata)

    def tick(self):
        if self.adminState==AdministratorState.INIT:
            self.setState(AdministratorState.ACTIONS)
            self.triggerAutotick()
        elif self.adminState==AdministratorState.ACTIONS:
            self.dequeueActions()
            self.genTasks()
            self.setState(AdministratorState.TASKS)
        elif self.adminState==AdministratorState.TASKS:
            self.genJobs()
            self.setState(AdministratorState.JOBS_TO_RUN)
        elif self.adminState==AdministratorState.JOBS_TO_RUN:
            self.setState(AdministratorState.JOBS)
           
            self.triggerJobs()
            
             

    def getStats(self):
        stats=Stats()
        stats.queuedActions=len(self.actionAdmin.actionQueue)
        stats.adminState=self.adminState
        
        for ac in self.actionAdmin.actions:
            if ac.isFinalState():
                stats.finishedActions+=1
            else:
                stats.activeActions+=1
        
        for task in self.tasksAdmin.tasks:
            if task.isFinalState():
                stats.finishedTasks+=1
            else:
                stats.activeTasks+=1

        for jobs in self.jobAdmin.jobs:
            if jobs.isFinalState():
                stats.finishedJobs+=1
            else:
                stats.activeJobs+=1
              
        return stats
         
    def addActionToQueue(self,name,actionType):
        ac=Action(self.actionCounter.increment(),name,ActionType[actionType])
        self.actionAdmin.addActionToQueue(ac)
        return ac

    def dequeueActions(self):
        self.actionAdmin.dequeueActions()

    def toStr(self):
        retThis=""
        for ac in self.actionAdmin.actions:
            retThis+=str(ac.toStr()+"\r")
        return retThis

    def addTask(self,task):       
        self.tasksAdmin.add(task)
        self.actionAdmin.upTaskCounterByActionID(task.actionID)

    def addTasks(self,taskList):      
        for task in taskList: 
             self.addTask(task)

    def addJob(self,job):       
        self.jobAdmin.addJob(job)
        
    
    def genTasks(self): 
        #errors first  
        logger.warning("Add failed tasks from the previous run")
        for task in self.tasksAdmin.tasks:    
            if task.state==TaskState.FAILED:
                self.tasksAdmin.markToRetry(task.id) 
                       
        logger.warning("Add new tasks")
        for ac in self.actionAdmin.actions:
            if ac.state==ActionState.PENDING:
                if ac.actionType==ActionType.MNR:
                    self.addTasks(MNRHelper().createTasks(ac))
                elif ac.actionType==ActionType.REBOOT:
                    self.addTasks(RebootHelper().createTasks(ac))
                ac.state=ActionState.TASKS_CREATED
        return self.tasksAdmin.toJSON()

    def genJobs(self):      
        for task in self.tasksAdmin.tasks:
            if task.state==TaskState.PENDING:
                if task.taskType==TaskType.MNR_MULTIPLE:
                    self.addJob(MNRHelper().createJobFromTask(task))
                elif task.taskType==TaskType.MNR_SINGLE:
                    self.addJob(MNRHelper().createJobFromTask(task))
                elif task.taskType==TaskType.REBOOTBATCH:
                    self.addJob(RebootHelper().createJobFromTask(task))
                task.state=TaskState.JOB_CREATED
        return self.jobAdmin.toJSON() 
    
    def cleanupJobs(self):
        finalJobs=0
        for job in self.jobAdmin.jobs:            
            if self.executor.futures.done(job.jobKey):
                future=self.executor.futures.pop(job.jobKey)
                job.jobresult=future.result()
                job.state=JobState.ENDED
                self.tasksAdmin.setTaskResult(job.task.id,job.remoteResult)
                if (job.remoteResult!= 1):
                    self.tasksAdmin.setTaskState(job.task.id,TaskState.FAILED)
                else:
                    self.tasksAdmin.setTaskState(job.task.id,TaskState.JOB_FINISHED)
            if job.isFinalState():
                finalJobs+=1
        if finalJobs==len(self.jobAdmin.jobs):
            self.setState(AdministratorState.ACTIONS)
            
        for task in self.tasksAdmin.tasks:
            if task.state==TaskState.JOB_FINISHED:            
                tasksLeft=self.actionAdmin.downTaskCounterByActionID(task.actionID)
                self.tasksAdmin.setTaskState(task.id,TaskState.ENDED)                
                if tasksLeft==0:
                    self.actionAdmin.setActionToDone(task.actionID)
        for ac in self.actionAdmin.actions:
            if  ac.state!=ActionState.PENDING:                                       
                if ac.tasksToGo==0:
                    ac.state=ActionState.ENDED



    def triggerJobs(self):
        self.cleanupJobs()
        for job in self.jobAdmin.jobs:
            if job.state==JobState.PENDING:
                job.setJobKey(job.name+"-"+str(job.id))
                fn=self.executor.submit_stored(job.jobKey, self.myBackGroundTask,job)
                fn.add_done_callback(self.callBack)
                job.state=JobState.TRIGGERED

    def callBack(self,future):
        print ("Callback")
        print ("Future",future.done())
        self.lastUpdate=time.time()
        self.cleanupJobs()
 
    def myBackGroundTask(self,job):        
        startTime=time.time()
        job.state=JobState.REMOTE_CALL_ONGOING
        print ("Dah"+str(job.name) )
        time.sleep(random.random()*10)
        print ("Duh"+str(job.name))
        
        job.remoteResult=random.randint(1, 3)  
        job.state=JobState.REMOTE_CALL_COMPLETE     
        job.runTime=time.time()-startTime
        
        return True   

    def triggerAutotick(self):
        fn=self.executor.submit(self.autoTickTask)

    def autoTickTask(self): 
        while 1==1:
            print ("yac")
            self.tick()
            time.sleep(5)

    def toJSON(self):
        return jsons.dumps(self)      

    