$("#save").click(function() {
    var rowCount = $("#boxes tr").length-1
    console.log(rowCount)
    var dataToSend = []
    for(var i=1; i<=rowCount; i++ ){
        //dataToSend.push(JSON.stringify({id: $("#boxes tr")[i].cells[0].textContent, 
                                        //addr: $("#address_field" + i + " :selected").text()}))
        // console.log($("#boxes tr")[i].cells[0].textContent)
        // console.log($("#address_field" + i + " :selected").text())
        dataToSend.push({id: $("#boxes tr")[i].cells[0].textContent, 
                        addr: $("#address_field" + i + " :selected").text()});
    }
    console.log(JSON.stringify(dataToSend))

    sendPOST('/config/replace', JSON.stringify({data: dataToSend}))
});


async function sendPOST(url, data){
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: data,
    });

    console.log(response)
}

async function fetchData(url){
	const response = await fetch(url);
	const datapoints = await response.json();
	console.log(datapoints);
	return datapoints;
};

function updateChart(start, end, id){
	const url = '/get/' + id + '?'+ 'start=' + start+':00' + '&' + 'end='+end+':00';
	

	fetchData(url).then(datapoints => {
		dateTemp = datapoints.data.map(function(e){
			//alert(e["date"]);
			return {x: e["date"], y: e["temp"]}
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

