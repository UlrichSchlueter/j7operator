from enum import Enum
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
from JobAdmin import JobRemoteState

from AtomicCounter import AtomicCounter


class ActionState(Enum):
    PENDING = 1
    TASKS_CREATED = 2
    ONGOING = 3
    ENDED = 4
    FAILED = 5

class ActionType(Enum):
    MNR = 1
    SWUPGRADE = 2
    REBOOT = 3
    PATCH = 4

   

class Action():
   
    def __init__(self, id,name, actionType):
        self.name=name
        self.id=id
        self.state=ActionState.PENDING
        self.actionType=actionType
        self.tasksToGo=0
        self.startTime=datetime.datetime.now()
        

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
        self.actionCounter= AtomicCounter()                
        

    def addAction(self,name,actionType):
        ac=Action(self.actionCounter.increment(),name,actionType)
        self.actions.append(ac)
        return ac

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
        

    def toJSON(self):
        return jsons.dumps(self)      

    