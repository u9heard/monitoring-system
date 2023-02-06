var apiURL = '/api/get';
var request = new XMLHttpRequest();
var req = apiURL;
var res;
var chart;

request.open('GET', req);
request.responseType = 'json';

request.send();

request.onload = await function() {
  res=request.response;
  plotChart();
  //alert(res.data)
};

function plotChart(){
  var data = res.data.map(function(e){
    return {x: e["date"], y: e["temp"]}
});


  var canvas = document.getElementById('myChart');
  var ctx = canvas.getContext('2d');
  var config = {
    type: 'line',
    data: {
      
      datasets: [{
          label: 'Graph Line',
          data: data,
          backgroundColor: 'rgba(0, 119, 204, 0.3)'
      }]
    },
    options: {
      scales: {
        x: {
          type: 'time',
          time: {
            unit: "hour",
            displayFormats: {
              hour: 'dd/MM/yyyy hh:mm:ss'
            }
          }
        }
      }
    }
  };

  chart = new Chart(ctx, config);

}
  
