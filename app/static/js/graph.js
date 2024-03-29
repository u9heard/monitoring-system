export var config = {
	type: 'line',
	data: {
	  
	  datasets: [{
		  label: 'Температура',
		  data: [],
		  borderColor: '#FF0000',
			backgroundColor: '#FF0000',
		  yAxisID: 'y2',
		  xAxisID: 'x2',
		  pointRadius: 0,
		  borderWidth: 1,
		  },
		  {
			  label: 'Влажность',
			  data: [],
			  borderColor: '#0000FF',
				backgroundColor: '#0000FF',
			  yAxisID: 'y',
			  pointRadius: 0,
			  borderWidth: 1,
		  }
	  ]
	},
	options: {
	spanGaps: 300000,
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
			  maxRotation: 45,
			  minRotation: 0,
			  
		  },
		  grid: {
			display: false,
			drawOnChartArea: true,
			drawTicks: true,
			tickWidth: 1,
			  //offset: true,
			  tickColor: '#000000',
		  }
		  
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
			  tickWidth: 3,
			  //offset: true,
			  tickColor: '#000000',
			  z: 1,
			  //display: true,
				// drawOnChartArea: true,
				// drawTicks: true,
		  },
		  ticks: {
			  padding: 8,
			  
			  includeBounds: false,
			  maxRotation: 45,
			  minRotation: 0,
			  
		  },
		  grid: {
			
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
		  
		  min: 20,
		  max: 80,
		  
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
		  min: 15,
		  max: 40,
		  
		  ticks: {
			  includeBounds: false,
			  maxRotation: 0,
			  minRotation: 0,
		  },
		  title:{
			  display: true,
			  text: "Температура, °C",
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
			  text: ["Температура, °C,","Влажность, %"],
			  font: {size: 16},
		  },
		  legend:{
			  display: false,
		  },
		  annotation: {
			annotations: {
				boxTemp: {
					type: 'box',
					mode: 'horizontal',
					yScaleID: 'y2',
					yMin: 37.5,
					yMax: 38.5,
					backgroundColor: 'rgba(0, 200, 0, 0.10)',
					// label: {
					//   content: 'My Horizontal Line',
					//   enabled: true
					// }
				},
				boxHum: {
					type: 'box',
					mode: 'horizontal',
					yScaleID: 'y',
					
					yMin: 65,
					yMax: 75,
					backgroundColor: 'rgba(0, 200, 0, 0.10)',
					// label: {
					//   content: 'My Horizontal Line',
					//   enabled: true
					// }
				  }
				},
				
			},
		  },
	  }
	};

