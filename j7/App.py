import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import logging

from flask import Flask
from flask_executor import Executor
from flask import render_template
from flask import request

import json

import mylogging 
from ActionAdmin import ActionAdmin
from ActionAdmin import Action
from TaskAdmin import TaskAdmin
from TaskAdmin import Task
from JobAdmin import JobAdmin
from JobAdmin import Job
from Administrator import Administrator
import datetime


logger = logging.getLogger('j7')
logger.warning('Appp This will get logged to a file')

print ("Hello __main")
print (sys.path)
print (dir())


app = Flask(__name__)

executor = Executor(app)
tasks= TaskAdmin()
jobs = JobAdmin()
actions = ActionAdmin()
administrator = Administrator(app,executor, tasks,jobs, actions)
#socketio = SocketIO(app)

currentTab="Dashboard"

def defaultDateFormatter(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y %H:%M"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)

def rerender():
    stats=administrator.getStats()   
    with app.open_resource('log/app.log') as f:
        logs = f.readlines()
        
    return render_template('index.html', currentPage=currentTab, actions=actions, tasks=tasks.tasks, jobs=jobs.allJobs(), executor=executor,stats=stats, logs=logs)

@app.route('/tasks')
def genTasks():
    administrator.dequeueActions()
    res=administrator.genTasks()
    return rerender()

@app.route('/stateInfo')
def getStateInfo():
 
    return render_template('stateInfo.html', administrator=administrator)

@app.route('/tick')
def doTick():
    administrator.tick()
    return rerender()

@app.route('/jobs')
def genJobs():
    res=administrator.genJobs()
    return rerender()

@app.route('/jobs/run')
def triggerJobs():
   
    res=administrator.triggerJobs()
    return rerender()    

@app.route('/Logs')
def getLogs():
    
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

@app.route('/queueUpdate')
def queueUpdate():    
    return render_template('actionsQueue.html', actions=actions)    



@app.route('/statUpdate')
def statsUpdate():    
    stats=administrator.getStats()
    return render_template('overview.html', stats=stats)            

@app.route('/getGraphData')
def getGraphData():    
    labels, data=jobs.getJobsStats()

    graphData={ 'labels' :labels, 'data' : data    }

    return json.dumps(graphData)

@app.route('/getActionGraphData')
def getActionGraphData():    
    #https://github.com/fanthos/chartjs-chart-timeline/wiki
    #labels, data=jobs.getJobsStats()
    labels = [ "test", "test2" ]
    datasets =[ { "data": [ [
                      "2018-01-21T16:00:00.000Z",
                      "2018-01-22T05:40:44.626Z",
                      "Unknown"
                         ]   ,
                        [
                      "2018-01-22T16:00:00.000Z",
                      "2018-01-23T05:40:44.626Z",
                      "Unknown"
                        ]
                        ] ,
                    "tag": "test3"
                  }
                ,
                {
                "data":[  [
                      "2018-01-22T16:00:00.000Z",
                      "2018-01-23T05:40:44.626Z",
                      "Unknown"
                        ]   ]                                
                  }
            ]
    labels, datasets=actions.actionStats.getData()
    graphData={ 'labels' : labels, 'datasets' : datasets   }

    return json.dumps(graphData, default=defaultDateFormatter)
        

@app.route('/')
def index():
    
    print ("tab "+currentTab)
    return rerender()   

@app.route('/menu/<tabName>')
def menu(tabName):
    global currentTab
    currentTab=tabName
    return rerender()  



@app.route('/test1', methods=['POST', 'GET'])
def test1():

    administrator.addActionToQueue("test1","MNR")
    return rerender()

@app.route('/test2', methods=['POST', 'GET'])
def test2():    
    administrator.addActionToQueue("test2","REBOOT")
    
    return rerender()


if __name__ == '__main__':
    print ("Here")
    #socketio.run(app, debug=True)
    app.run(debug=True)    