function predictPrice(){
  $("div.price").removeClass("hidden");
  km = $("input#inputKm")[0].value;
  age = $("input#inputYear")[0].value;
  model = $("select#inputModel")[0].value;
  seller = $("select#inputSell")[0].value;
  trans = $("select#inputTrans")[0].value;
  owner = $("select#inputOwner")[0].value;
  fuel = $("select#inputFuel")[0].value;
  city = $("select#inputCity")[0].value;
  body = $("select#inputBody")[0].value;
  color = $("select#inputColor")[0].value;

  km = km == "" ? 0 : km;
  age = age =="" ? 0 : age;

  param =  {"KmNumeric":km,
  "MakeYear":age,
  "OwnerTypeId":owner,
  "BodyStyleId":body,
  "Seller":seller,
  "GearBox":trans,
  "Fuel":fuel,
  "Color":color,
  "RootName":model,
  "CityName":city
};

// send ajax request
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    document.getElementById('priceSpan').innerHTML = this.responseText;
    console.log(this.responseText);
  }
};
// xhttp.open("GET", "http://127.0.0.1:5002/test", true);

xhttp.open("POST", "http://127.0.0.1:5002/test",true);
xhttp.setRequestHeader("Content-Type", "application/json");
xhttp.send(JSON.stringify(param));
}


var chart1;
d3.csv('data.csv', function(error, data) {
    data.forEach(function (d) {
        d.value = +d.value;
    });
    chart1 = makeDistroChart({
        data:data,
        xName:'date',
        yName:'value',
        axisLabels: {xAxis: 'Years', yAxis: 'Values'},
        selector:"#chart-distro1",
        chartSize:{height:460, width:960},
        constrainExtremes:true});
    chart1.renderBoxPlot();
    chart1.renderDataPlots();
    chart1.renderNotchBoxes({showNotchBox:false});
    chart1.renderViolinPlot({showViolinPlot:false});
});