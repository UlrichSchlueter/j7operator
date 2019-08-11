
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


function myTimer() {
    var d = new Date();
    var xhttp = new XMLHttpRequest();
    var jobsXhttp = new XMLHttpRequest();
    var tasksXhttp = new XMLHttpRequest();
    var actionsXhttp = new XMLHttpRequest();
    var overviewXhttp = new XMLHttpRequest();
    var grapshUpdateXhttp=new XMLHttpRequest();


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

                overviewXhttp.open("GET", '/statUpdate', true);
                overviewXhttp.send();

                grapshUpdateXhttp.open("GET", '/getGraphData', true);
                grapshUpdateXhttp.send();


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

            grapshUpdateXhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var myObj = JSON.parse(this.responseText);
                    if (myChart === undefined) { createChart () }
                    myChart.data.datasets[0].data = myObj.data;
                    myChart.data.labels = myObj.labels;

                    myChart.update();
                }};
  
  
  xhttp.open("GET", '/isUpdated', true);
  xhttp.send();
  
  
  
}
}())