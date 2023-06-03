$("#save").click(async function() {
    var rowCountSys = $("#boxes tr").length-1
    var rowCountDev = $("#corrections tr").length-1
    console.log(rowCountSys)
    var boxToSend = []
    var deviceToSend = []
    for(var i=1; i<=rowCountSys; i++ ){

        boxToSend.push({box_active: $("#box_active" + i).is(':checked') ? 1 : 0, alert_active: $("#alert_active" + i).is(':checked') ? 1 : 0, id: $("#boxes tr")[i].cells[2].textContent, 
                        addr: $("#address_field" + i + " :selected").text()});
    }
    for(var i=1; i<=rowCountDev; i++){
        var ids = $("#corrections tr")[i].cells[0].textContent
        deviceToSend.push({id: ids, 
                        correction_t: $("#cor_t_field" + ids).val(),
                        correction_h: $("#cor_h_field" + ids).val()});
    }
    console.log(JSON.stringify({box: boxToSend, device:deviceToSend}))

    const res = await sendPOST('api/config/replace', JSON.stringify({box: boxToSend, device:deviceToSend}))
    
    location.reload(true);
});


$('body').on('input', '.input', function(){
	this.value = this.value.replace(/[^0-9\.]/g, '');
});

async function sendPOST(url, data){
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: data,
    });

    const respJson  = await response.json()
    console.log(respJson)
}



