var update;
var ctx = document.getElementById('myChart');
var chart;
var dataTemp = [{x: '2021-06-01 15:00:00', y: 20}];
var dataHum = [{x: '2021-06-01 15:00:00', y: 20}];
var config = {
  type: 'line',
  data: {
	
	datasets: [{
		label: 'Температура',
		data: dataTemp,
		borderColor: '#FF0000',
      	backgroundColor: '#FF0000',
		yAxisID: 'y2',
		xAxisID: 'x2',
		pointRadius: 0,
		borderWidth: 1,
		},
		{
			label: 'Влажность',
			data: dataHum,
			borderColor: '#0000FF',
      		backgroundColor: '#0000FF',
			yAxisID: 'y',
			pointRadius: 0,
			borderWidth: 1,
		}
	]
  },
  options: {
	responsive: true,
	scales: {
	  x: {
		type: 'time',
		time: {
		  unit: "minute",
		  displayFormats: {
			minute: 'dd.MM.yyyy hh:mm:ss'
		  },
		  tooltipFormat: "dd.MM.yyyy kk:mm:ss"
		},
		offset: true,
		position: 'center',
		border: {
			width: 1,
			color: '#000000',
		},
		ticks: {
			display: false,
			includeBounds: false,
			maxRotation: 0,
			minRotation: 0,
			
		},
		
	  },
	  x2: {
		
		type: 'time',
		time: {
		  unit: "minute",
		  displayFormats: {
			hour: "hh",
			minute: 'dd.MM.yyyy kk:mm:ss'
		  },
		  tooltipFormat: "dd.MM.yyyy kk:mm:ss"
		},
		offset: true,
		position: 'bottom',
		border: {
			
			width: 1,
			color: '#000000',
		},
		grid: {
			tickWidth: 1,
			//offset: true,
			tickColor: '#000000',
			z: 1
		},
		ticks: {
			padding: 8,
			
			includeBounds: false,
			maxRotation: 0,
			minRotation: 0,
			
		}
		
	  },
	  y: {
		type: 'linear',
		positon: 'left',
		stack: 'demo',
		stackWeight: 1,
		border: {
			width: 1,
			color: '#000000',
		},
		grid: {
			tickWidth: 1,
			//offset: true,
			tickColor: '#000000',
		},
		
		min: 50,
		max: 90,
		
		ticks: {
			includeBounds: false,
			maxRotation: 0,
			minRotation: 0,
		},
		title:{
			display: true,
			text: "Влажность, %",
			color: "black",
			font:{
				size: 14,
				weight: "bold"
			}
		}
	  },
	  y2: {
		type: 'linear',
		offset: true,
		position: 'left',
		stack: 'demo',
		stackWeight: 1,
		border: {
			width: 1,
			color: '#000000',
		},
		grid: {
			tickWidth: 1,
			//offset: true,
			tickColor: '#000000',
			
		},
		min: 50,
		max: 110,
		
		ticks: {
			includeBounds: false,
			maxRotation: 0,
			minRotation: 0,
		},
		title:{
			display: true,
			text: "Температура, °F",
			color: "black",
			font:{
				size: 14,
				weight: "bold"
			}
		}
	  }
	},
	plugins:{
		title:{
			display: true,
			color: 'black',
			text: ["Температура, °F,","Влажность, %"],
			font: {size: 16},
		},
		legend:{
			display: false,
		}
	}
  }
};

async function fetchData(url){
	const response = await fetch(url);
	const datapoints = await response.json();
	// console.log(datapoints);
	return datapoints;
};

function updateChart(id){
	const url = '/indications/' + id;
	

	fetchData(url).then(datapoints => {
		dateTemp = datapoints.data.map(function(e){
			//alert(e["date"]);
			return {x: e["date"], y: e["temp"], y2:e["hum"]}
		});

		dateHum= datapoints.data.map(function(e){
			//alert(e["date"]);
			return {x: e["date"], y:e["hum"]}
		});

		chart.data.datasets[0].data = dateTemp;
		chart.data.datasets[1].data = dateHum;
		chart.update();
	});
};

function clearChartData(){
	chart.data.datasets[0].data = [];
}

$(document).ready(function() {
	var boxData;
	fetchData("indications/last").then(datapoints => {

		

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












