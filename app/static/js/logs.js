import { config } from "./graph.js"

var temp
var hum

async function fetchData(url){
	const response = await fetch(url);
	const datapoints = await response.json();
	// console.log(datapoints);
	return datapoints;
};

$(".openPopup").on('click',
function(){
    $('#myPopup').css('display', 'block');
    
    fetchData('/api/logs/' + $(this).data('id')).then(datapoints => {
		temp = datapoints.map(function(e){
			//alert(e["temp"]);
			return {x: e["time"], y: e["temp"], y2:e["hum"]}
		});

		hum = datapoints.map(function(e){
			//alert(e["date"]);
			return {x: e["time"], y:e["hum"]}
		});

		chart.data.datasets[0].data = temp;
		chart.data.datasets[1].data = hum;
		chart.update();
		chart.resize();
	});

    fetchData('/api/logs/' + $(this).data('id')).then(datapoints => {
		temp = datapoints.map(function(e){
			//alert(e["temp"]);
			return {x: e["time"], y: e["temp"], y2:e["hum"]}
		});

		hum = datapoints.map(function(e){
			//alert(e["date"]);
			return {x: e["time"], y:e["hum"]}
		});

		chart.data.datasets[0].data = temp;
		chart.data.datasets[1].data = hum;
		chart.update();
	});
}
);

$(".close").on('click',
function(){
    $('#myPopup').css('display', 'none');
}
);

var ctx = document.getElementById('myChart');

var chart = new Chart(ctx, config);