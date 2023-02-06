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
			minute: 'dd/MM/yyyy hh:mm:ss'
		  }
		},
		offset: true,
		position: 'center',
		border: {
			width: 1,
			color: '#000000',
		},
		ticks: {
			display: false,
		},
	  },
	  x2: {
		
		type: 'time',
		time: {
		  unit: "minute",
		  displayFormats: {
			minute: 'dd/MM/yyyy hh:mm:ss'
		  }
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
		
	  },
	  y2: {
		type: 'linear',
		offset: false,
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
	  }
	}
  }
};

function updateChart(id){
	const url = 'api/get/' + id;
	async function fetchData(url){
		const response = await fetch(url);
		const datapoints = await response.json();
		console.log(datapoints);
		return datapoints;
	};

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
		$('.map rect').attr('class', '');
		$('.map rect[data-id=' + $(this).data('id') + ']').attr('class', 'active');
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












