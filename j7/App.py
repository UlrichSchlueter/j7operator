import sys
from os.path import dirname
sys.path.append(dirname(__file__))

from flask import Flask
from flask_executor import Executor
from flask import render_template
from flask import request

import json


from ActionAdmin import ActionAdmin
from ActionAdmin import Action
from TaskAdmin import TaskAdmin
from TaskAdmin import Task
from JobAdmin import JobAdmin
from JobAdmin import Job
from Administrator import Administrator



print ("Hello __main")
print (sys.path)
print (dir())


app = Flask(__name__)

executor = Executor(app)
tasks= TaskAdmin()
jobs = JobAdmin()
actions = ActionAdmin()
administrator = Administrator(executor, tasks,jobs, actions)
#socketio = SocketIO(app)

currentTab="Dashboard"

@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y %H:%M"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)

def rerender():
    stats=administrator.getStats()   
       
    return render_template('index.html', currentPage=currentTab, actions=actions, tasks=tasks.tasks, jobs=jobs.allJobs(), executor=executor,stats=stats)

@app.route('/tasks')
def genTasks():
    # Do signup form s
    res=administrator.genTasks()
    
    return rerender()

@app.route('/jobs')
def genJobs():
    res=administrator.genJobs()
    return rerender()

@app.route('/jobs/run')
def triggerJobs():
   
    res=administrator.triggerJobs()
    return rerender()    




@app.route('/actions')
def listAction():
    # Do signup form s

    return actions.toJSON()

@app.route('/isUpdated')
def isUpdated():
    return str(administrator.lastUpdate)
        

@app.route('/jobsUpdate')
def jobsUpdate():    
    return render_template('jobs.html', jobs=jobs.allJobs(), executor=executor)    

@app.route('/tasksUpdate')
def tasksUpdate():      
    return render_template('tasks.html', tasks=tasks.tasks)    

@app.route('/actionsUpdate')
def actionsUpdate():    
    return render_template('actions.html', actions=actions)    

@app.route('/statUpdate')
def statsUpdate():    
    stats=administrator.getStats()
    return render_template('overview.html', stats=stats)            

@app.route('/getGraphData')
def getGraphData():    
    labels, data=jobs.getJobsStats()

    graphData={ 'labels' :labels, 'data' : data    }

    return json.dumps(graphData)
        

@app.route('/')
def index():
    
    print ("tab "+currentTab)
    return rerender()   

@app.route('/menu/<tabName>')
def menu(tabName):
    global currentTab
    print ("tab1 "+currentTab)  
    currentTab=tabName
    print ("tab2 "+currentTab)     
    return rerender()  

    #return render_template('dash.html', actions=actions, tasks=tasks, jobs=jobs.activeJobs(), executor=executor)



@app.route('/test1', methods=['POST', 'GET'])
def test1():
         
    administrator.addAction("test1","MNR")
    #socketio.send("GGH") 
    return rerender()

@app.route('/test2', methods=['POST', 'GET'])
def test2():    
    administrator.addAction("test2","MNR")
    genTasks()
    genJobs()
    triggerJobs()
    return rerender()


if __name__ == '__main__':
    print ("Here")
    #socketio.run(app, debug=True)
    app.run(debug=True)    