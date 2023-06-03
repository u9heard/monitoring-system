import { config } from "./graph.js"

var temp
var hum
var ctx = document.getElementById('myChart');
var chart;


async function fetchData(url){
	const response = await fetch(url);
	const datapoints = await response.json();
	console.log(datapoints);
	return datapoints;
};

function plotChart(name){

}

function updateChart(start, end, id){
	const url = '/api/indications/' + id + '?'+ 'start=' + start+':00' + '&' + 'end='+end+':00';
	

	fetchData(url).then(datapoints => {
		temp = datapoints.map(function(e){
			//alert(e["date"]);
			return {x: e["time"], y: e["temp"]}
		});

		hum= datapoints.map(function(e){
			//alert(e["date"]);
			return {x: e["time"], y:e["hum"]}
		});

		chart.data.datasets[0].data = temp;
		chart.data.datasets[1].data = hum;
		chart.update();
		chart.resize();
	});
};

function clearChartData(){
	chart.data.datasets[0].data = [];
}


$("#preview").click(function() {
    var start = $('#date_start').val();
	var end = $('#date_end').val();
	$('canvas').css('display', 'block');
	var r = $('#box_field').val();
	updateChart(start, end, $('option[value='+r+']').text());
});

chart = new Chart(ctx, config);


$('#screen').click(function() {
	var a = document.createElement('a');
	a.href = chart.toBase64Image();
	a.download = 'graph.jpeg';

	a.click()
});

