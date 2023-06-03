import { config } from "./graph.js"

var temp
var hum
var update;
var ctx = document.getElementById('myChart');
var chart;

async function fetchData(url){
	const response = await fetch(url);
	const datapoints = await response.json();
	// console.log(datapoints);
	return datapoints;
};

function updateChart(id){
	const url = 'api/indications/' + id;
	

	fetchData(url).then(datapoints => {
		temp = datapoints.map(function(e){
			//alert(e["temp"]);
			return {x: e["time"], y: e["temp"], y2:e["hum"]}
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

$(document).ready(function() {
	var boxData;
	fetchData("api/indications/last").then(datapoints => {

		

		datapoints.forEach(function(e) { 
			
			$('.map rect[data-id=' + e.name + ']').addClass('green');
			$('.map-item[data-id=' + e.name + ']').find('.map-popup').text("Online");
			$('.map-item[data-id=' + e.name + ']').find('.map-popup').css({'color': 'green'});
		});
	});

})

$('.map rect').hover( 
	function(){
		
		$('.map-item[data-id=' + $(this).data('id') + ']').find('.map-popup').show();
		
	},
	function(){
		$('.map-item[data-id=' + $(this).data('id') + ']').find('.map-popup').hide();
	}
);

$('.map-item').hover(
	function(){
		$('.map rect[data-id=' + $(this).data('id') + ']').attr('id', 'hover');
		
		$(this).find('.map-popup').show();
	},
	function(){
		$('.map rect[data-id=' + $(this).data('id') + ']').attr('id', '');
		
		$(this).find('.map-popup').hide();
	}
);	

$('.map-item').on('click',
	function(){
		$('.map rect').removeClass('active');
		$('.map rect[data-id=' + $(this).data('id') + ']').addClass('active');
		// $('.map rect').attr('class', '');
		// $('.map rect[data-id=' + $(this).data('id') + ']').attr('class', 'active');
		$('canvas').css('display', 'block');
		clearChartData();
		clearInterval(update);
		update = setInterval(() => updateChart($(this).data('id')), 1500);
	}
);

$('.map rect').on('click',
	function(){
		$('.map-item[data-id=' + $(this).data('id') + ']').trigger('click');
	}
);




chart = new Chart(ctx, config);












