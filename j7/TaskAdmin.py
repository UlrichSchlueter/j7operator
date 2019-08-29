from enum import Enum, auto
import jsons
import datetime
from AtomicCounter import AtomicCounter


class TaskState(Enum):
        PENDING = auto()
        JOB_CREATED =  auto()
        JOB_FINISHED =  auto()
        ONGOING =  auto()
        ENDED =  auto()
        FAILED =  auto()

class TaskType(Enum):
    MNR_SINGLE = auto()
    MNR_MULTIPLE = auto()
    SWUPGRADEBATCH = auto()
    REBOOTBATCH = auto()
    PATCHBATCH = auto()
    NONE=auto()

class TaskErrorStrategy(Enum):
    RETRY_ONCE = auto()
    RETRY_TWICE = auto()
    NONE = auto()
    
        
taskCounter= AtomicCounter()            




class Task:
    def __init__(self, name, actionID,taskType):
        self.name=name
        self.id=taskCounter.increment()
        self.state=TaskState.PENDING
        self.actionID=actionID
        self.iterations=0
        self.taskType=taskType
        self.taskResult=None
        self.startTime=datetime.datetime.now()
        self.stopTime=None

    def isFinalState(self):
        if self.state==TaskState.ENDED:
            return True
        else:
            return False   

    def isInErrorState(self):
       
        if self.state==TaskState.FAILED:
            return True
        else:
            return False     

    def toJSON(self):
        return jsons.dumps(self)            

class TaskAdmin:
    def __init__(self):
        self.tasks=[]       

    def add(self,task):
        self.tasks.append(task)
        return task

    def getByActionID(self,id):
        rcThis=[]
        for t in self.tasks:
            if t.actionID==id:
                rcThis.append(t)
        return rcThis

    def findTaskByID(self,id):
        task=None
        for t in self.tasks:
            if t.id==id:
                task=t
                break
        return task

    def activeTasks(self):
        activeTasks=[]
        for task in self.tasks:
            if not task.isFinalState():
                activeTasks.append(task)
        return activeTasks        

    def setTaskResult(self,id,result):        
        for t in self.tasks:
            if t.id==id:
                t.taskResult=result
                break
    
    def setTaskState(self,id,state):
        t=None
        for t in self.tasks:
            if t.id==id:
                t.state=state
                if t.isFinalState():                   
                    t.stopTime=datetime.datetime.now()
                break
        return t

    def markToRetry(self,id):
        task=self.findTaskByID(id)
        task.state=TaskState.PENDING
        task.iterations+=1
        task.taskResult=None

    def toJSON(self):
        return jsons.dumps(self)            

