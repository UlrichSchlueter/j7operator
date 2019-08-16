from enum import Enum,auto
import datetime
import jsons
from AtomicCounter import AtomicCounter


jobsCounter= AtomicCounter()    

class JobState(Enum):
    PENDING = auto()
    TRIGGERED = auto()
    REMOTE_CALL_ONGOING = auto()        
    REMOTE_CALL_COMPLETE = auto()
    FAILED = auto()
    ENDED = auto()

class JobRemoteResult(Enum):
        OK = 1
        FAILED_ABORT = 2
        FAILED_RETRY = 3               
            

class JobType(Enum):
    REST = 1
    SOAP = 2
    COMMAND = 3
    AWX = 4
    

class JobStats():
    def __init__(self):
        self.stats=[]

class Job:
    def __init__(self, name, task,jobType, jobParams):
        self.name=name
        self.id=jobsCounter.increment()
        self.state=JobState.PENDING
        self.task=task
        self.jobType=jobType
        self.jobParams=jobParams
        self.jobKey=""
        self.futureExecutionStatus=None
        self.futureExecutionResult=None
        self.remoteState=None
        self.remoteResult=None
        self.runTime=0       
        self.startTime=datetime.datetime.now() 

    def isFinalState(self):
        if self.state in  [JobState.ENDED,JobState.FAILED]:        
            return True
        else:
            return False        
        
    def setJobKey(self,key):
        self.jobKey=key

    def toJSON(self):
        return jsons.dumps(self)            

class JobAdmin:
    def __init__(self):
        self.jobs=[]
        self.jobStats=JobStats()

    def addJob(self,job):        
        self.jobs.append(job)
       

    def getJobsStats(self):
        max=min(len(self.jobs),10)    
        labels=[]
        data=[]
        
        for i in range(0,max):
            job=self.jobs[-i]
            labels.append(str(job.id)+" "+job.name)
            data.append(job.runTime)
        return labels,data

    def activeJobs(self):
        activeJs=[]
        for job in self.jobs:
            if job.state != JobState.ENDED:
                activeJs.append(job)
        return activeJs

    def allJobs(self):        
        return self.jobs

    def toJSON(self):
        return jsons.dumps(self)            

