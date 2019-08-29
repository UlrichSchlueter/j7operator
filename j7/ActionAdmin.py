from enum import Enum, auto
import jsons
import time
import random
import datetime

from flask_executor import Executor

from TaskAdmin import TaskAdmin
from TaskAdmin import Task
from TaskAdmin import TaskType
from TaskAdmin import TaskState
from JobAdmin import JobAdmin
from JobAdmin import Job
from JobAdmin import JobType
from JobAdmin import JobState
from AtomicCounter import AtomicCounter


class ActionState(Enum):
    PENDING = auto()
    TASKS_CREATED = auto()
    ONGOING = auto()
    ENDED = auto()
    FAILED = auto()
    QUEUED = auto()

class ActionType(Enum):
    MNR = 1
    SWUPGRADE = 2
    REBOOT = 3
    PATCH = 4

class ActionStats:
    def __init__(self):
        self.labels=[]
        self.datasets=[]
        #self.addEntry("2018-01-22T16:00:00.000Z", "2018-01-23T05:40:44.626Z","Action1","task")
        #self.addEntry("2018-01-23T18:00:00.000Z", "2018-01-23T22:40:44.626Z","Action2","task")
        

    def addEntry(self, startTime, stopTime, actionName, taskName):
            targetDict=None
            for dataDict in self.datasets:
                if dataDict['tag']==actionName:
                    targetDict=dataDict
                    break
            if targetDict==None:
                targetDict={}
                self.datasets.append(targetDict)
                self.labels.append(actionName)    
            targetDict['data']=[]
            targetDict['tag']=actionName     
               
            targetDict['data'].append([startTime, stopTime, taskName])
   
    def getData(self):
        return self.labels, self.datasets

class Action():
   
    def __init__(self, id,name, actionType):
        self.name=name
        self.id=id
        self.state=ActionState.PENDING
        self.actionType=actionType
        self.tasksToGo=0
        self.startTime=datetime.datetime.now()
        self.stopTime=None
        

    def isFinalState(self):
        if self.state==ActionState.ENDED or self.state==ActionState.FAILED:
            return True
        else:
            return False

    def toJSON(self):
        return jsons.dumps(self)        
                
class ActionAdmin:   

    def __init__(self):
        self.actions=[]    
        self.actionQueue=[]    
        self.actionCounter= AtomicCounter()    
        self.actionStats=ActionStats()            
        

    def addActionToQueue(self,ac):
        ac.state=ActionState.QUEUED
        self.actionQueue.append(ac)
        return ac

    def dequeueActions(self):
        for ac in self.actionQueue:
            ac.state=ActionState.PENDING
            self.actions.append(ac)
            
        self.actionQueue=[] 


    def toStr(self):
        retThis=""
        for ac in self.actions:
            retThis+=str(ac.toStr()+"\r")
        return retThis

   

    def upTaskCounterByActionID(self,id):
        for ac in self.actions:
            if ac.id==id:
                ac.tasksToGo+=1
        return ac.tasksToGo

    def downTaskCounterByActionID(self,id):
        for ac in self.actions:
            if ac.id==id:
                ac.tasksToGo-=1
        return ac.tasksToGo
        

    def setActionToDone(self,actionID):
        for ac in self.actions:
            if ac.id==actionID:
                ac.state=ActionState.ENDED
                ac.stopTime=datetime.datetime.now()

    def addTaskStat(self, actionID,startTime, stopTime, taskName):
        for ac in self.actions:
            if ac.id==actionID:
                self.actionStats.addEntry(startTime, stopTime, "#"+str(actionID) + ":"+ac.name, taskName)
        

    def toJSON(self):
        return jsons.dumps(self)      

    