from ActionAdmin import Action
from TaskAdmin import TaskAdmin
from TaskAdmin import Task
from TaskAdmin import TaskType
from TaskAdmin import TaskState
from JobAdmin import JobAdmin
from JobAdmin import Job
from JobAdmin import JobType
from JobAdmin import JobState
from JobAdmin import JobRemoteState


class RebootHelper():

    def __init__(self):
        self.name="MNRHELPER"
    
    def createTasks(self, action):
        tasks=[]
        tasks.append(Task("task-"+action.name,action.id,TaskType.REBOOTBATCH))
        
        return tasks

    def createJobFromTask(self,task):
        job=None
        if (task.taskType==TaskType.REBOOTBATCH):
            job=self.handle_REBOOTBATCH_TaskType(task)        
        return job

    def handle_REBOOTBATCH_TaskType(self,task):
        return Job("job-"+str(task.taskType),task,JobType.AWX,"Param 1, param 2")

        

