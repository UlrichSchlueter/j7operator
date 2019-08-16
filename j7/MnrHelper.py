from ActionAdmin import Action
from TaskAdmin import TaskAdmin
from TaskAdmin import Task
from TaskAdmin import TaskType
from TaskAdmin import TaskState
from JobAdmin import JobAdmin
from JobAdmin import Job
from JobAdmin import JobType
from JobAdmin import JobState



class MNRHelper():

    def __init__(self):
        self.name="MNRHELPER"
    
    def createTasks(self, action):
        tasks=[]
        tasks.append(Task("task-single-"+action.name,action.id,TaskType.MNR_SINGLE))
        tasks.append(Task("task-"+action.name,action.id,TaskType.MNR_MULTIPLE))    
        tasks.append(Task("task-single-"+action.name,action.id,TaskType.MNR_SINGLE)) 
        return tasks

    def createJobFromTask(self,task):
        job=None
        if (task.taskType==TaskType.MNR_SINGLE):
            job=self.handle_MNR_SINGLE_TaskType(task)
        elif (task.taskType==TaskType.MNR_MULTIPLE):
            job=self.handle_MNR_MULTIPLE_TaskType(task)
        return job


    def handle_MNR_SINGLE_TaskType(self,task):
        return Job("job-"+str(task.taskType),task,JobType.REST,"Param 1, param 2")
           
    def handle_MNR_MULTIPLE_TaskType(self,task):
        return Job("job-"+str(task.taskType),task,JobType.REST,"Param 1, param 2")
        

