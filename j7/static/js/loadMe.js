
(function () {


var myVar = setInterval(myTimer, 2000);
var lastEpoch=""
var myChart



feather.replace()

function createChart() {
  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [        
      ],
      datasets: [{
        data: [          
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
}


function createActionsChart() {
  // Graphs
  var ctx = document.getElementById('actionChart')
  // eslint-disable-next-line no-unused-vars
  myChart = new Chart(ctx, {
    type: 'timeline',
    data: {
      labels: [  
        "None"      
      ],
      datasets: [{
        data: [          
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
       // "textPadding": 4
       animation: {
        duration: 0
        },
       "elements": {
        "colorFunction": function(text, data, dataset, index) {
            return Color('black');
        },
        "showText": true,
        "textPadding": 4
       
    }
    }
  })
}


function myTimer() {
    var d = new Date();
    var xhttp = new XMLHttpRequest();
    var jobsXhttp = new XMLHttpRequest();
    var tasksXhttp = new XMLHttpRequest();
    var actionsXhttp = new XMLHttpRequest();
    var queueXhttp = new XMLHttpRequest();
    var overviewXhttp = new XMLHttpRequest();
    var grapshUpdateXhttp=new XMLHttpRequest();
    var stateUpdateXhttp=new XMLHttpRequest();


    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200 ) {
            if (xhttp.responseText!=lastEpoch)
            {
                jobsXhttp.open("GET", '/jobsUpdate', true);
                jobsXhttp.send();

                tasksXhttp.open("GET", '/tasksUpdate', true);
                tasksXhttp.send();

                actionsXhttp.open("GET", '/actionsUpdate', true);
                actionsXhttp.send();

                queueXhttp.open("GET", '/queueUpdate', true);
                queueXhttp.send();

                overviewXhttp.open("GET", '/statUpdate', true);
                overviewXhttp.send();

                grapshUpdateXhttp.open("GET", '/getActionGraphData', true);
                grapshUpdateXhttp.send();

                stateUpdateXhttp.open("GET", '/stateInfo', true);
                stateUpdateXhttp.send();


                lastEpoch=xhttp.responseText
            }
        }
      };

      jobsXhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
         document.getElementById("jobs").innerHTML = this.responseText;
        } };

        tasksXhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
             document.getElementById("tasks").innerHTML = this.responseText;
            } };


        actionsXhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                 document.getElementById("actions").innerHTML = this.responseText;
                }};

        overviewXhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("Overview").innerHTML = this.responseText;
            }};

            stateUpdateXhttp.onreadystatechange = function() {
              if (this.readyState == 4 && this.status == 200) {
                  document.getElementById("StateInfo").innerHTML = this.responseText;
              }};
            
              queueXhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    document.getElementById("queue").innerHTML = this.responseText;
                }};

              

            grapshUpdateXhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var myObj = JSON.parse(this.responseText);
                    if (myChart === undefined) { createActionsChart () }
                    myChart.data.datasets = myObj.datasets;
                    myChart.data.labels = myObj.labels;

                    myChart.update();
                }};
  
  
  xhttp.open("GET", '/isUpdated', true);
  xhttp.send();
  
  
  
}
}())