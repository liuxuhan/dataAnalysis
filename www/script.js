function predictPrice() {
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
  age = age == "" ? 0 : age;

  param = {
    "KmNumeric": km,
    "MakeYear": age,
    "OwnerTypeId": owner,
    "BodyStyleId": body,
    "Seller": seller,
    "GearBox": trans,
    "Fuel": fuel,
    "Color": color,
    "RootName": model,
    "CityName": city
  };

  // send ajax request
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById('priceSpan').innerHTML = this.responseText;
      getCluster(param)
      console.log(this.responseText);
    }
  };
  // xhttp.open("GET", "http://127.0.0.1:5002/test", true);
  xhttp.open("POST", "http://127.0.0.1:5002/test", true);
  xhttp.setRequestHeader("Content-Type", "application/json");
  xhttp.send(JSON.stringify(param));
}

function getCluster(param) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText);
    }
  };
  xhttp.open("POST", "http://127.0.0.1:5002/getcluster", true);
  xhttp.setRequestHeader("Content-Type", "application/json");
  xhttp.send(JSON.stringify(param));
}

var chart1;

function showBox() {
  chart1.violinPlots.hide();
  chart1.boxPlots.show({
    reset: true
  });
  chart1.notchBoxes.hide();
  chart1.dataPlots.change({
    showPlot: false,
    showBeanLines: false
  });
}

function showNotched() {
  chart1.violinPlots.hide();
  chart1.notchBoxes.show({
    reset: true
  });
  chart1.boxPlots.show({
    reset: true,
    showBox: false,
    showOutliers: true,
    boxWidth: 20,
    scatterOutliers: true
  });
  chart1.dataPlots.change({
    showPlot: false,
    showBeanLines: false
  });
}

function showViolin() {
  chart1.violinPlots.show({
    reset: true,
    clamp: 0
  });
  chart1.boxPlots.show({
    reset: true,
    showWhiskers: false,
    showOutliers: false,
    boxWidth: 10,
    lineWidth: 15,
    colors: ['#555']
  });
  chart1.notchBoxes.hide();
  chart1.dataPlots.change({
    showPlot: false,
    showBeanLines: false
  });
}

function showClamp() {
  chart1.violinPlots.show({
    reset: true,
    clamp: 1
  });
  chart1.boxPlots.show({
    reset: true,
    showWhiskers: false,
    showOutliers: false,
    boxWidth: 10,
    lineWidth: 15,
    colors: ['#555']
  });
  chart1.notchBoxes.hide();
  chart1.dataPlots.change({
    showPlot: false,
    showBeanLines: false
  });
}

function showBean() {
  chart1.violinPlots.show({
    reset: true,
    width: 75,
    clamp: 0,
    resolution: 30,
    bandwidth: 50
  });
  chart1.dataPlots.show({
    showBeanLines: true,
    beanWidth: 15,
    showPlot: false,
    colors: ['#555']
  });
  chart1.boxPlots.hide();
  chart1.notchBoxes.hide();
}

function showBeeswarm() {
  chart1.violinPlots.hide();
  chart1.dataPlots.show({
    showPlot: true,
    plotType: 'beeswarm',
    showBeanLines: false,
    colors: null
  });
  chart1.notchBoxes.hide();
  chart1.boxPlots.hide();
}

function showScatter() {
  chart1.violinPlots.hide();
  chart1.dataPlots.show({
    showPlot: true,
    plotType: 40,
    showBeanLines: false,
    colors: null
  });
  chart1.notchBoxes.hide();
  chart1.boxPlots.hide();
}

function showLines() {
  if (chart1.dataPlots.options.showLines) {
    chart1.dataPlots.change({
      showLines: false
    });
  } else {
    chart1.dataPlots.change({
      showLines: ['median', 'quartile1', 'quartile3']
    });
  }
}

function toggleShow() {
  show_el = $("span.badge")
  if (show_el.hasClass('single')) {
    show_el.text("Show single:")
  } else {
    show_el.text("Show all:")
  }
  show_el.toggleClass('single');
  $('div.btn-group').toggleClass('hidden');

}

function creatChart(fileName) {
  d3.csv(fileName, function (error, data) {
    data.forEach(function (d) {
      d.value = +d.value;
    });
    chart1 = makeDistroChart({
      data: data,
      xName: 'date',
      yName: 'value',
      axisLabels: {
        xAxis: null,
        yAxis: 'Values'
      },
      selector: "#chart-distro1",
      chartSize: {
        height: 460,
        width: 960
      },
      constrainExtremes: true
    });
    chart1.renderBoxPlot();
    chart1.renderDataPlots();
    chart1.renderNotchBoxes({
      showNotchBox: false
    });
    chart1.renderViolinPlot({
      showViolinPlot: false
    });
  });
}

function showPage(pageName) {
  className = "div." + pageName + "Page";
  $('div.pages').addClass("hidden");
  $(className).removeClass("hidden");
  if (pageName == 'visual' && $("div.chart-wrapper").children().length == 0) {
    creatChart('data.csv');
  }
}

function validate() {
  if ($("input#inputKm")[0].value != "" && $("input#inputYear")[0].value != "") {
    document.getElementById("searchBtn").disabled = false;
  } else {
    document.getElementById("searchBtn").disabled = true;
  }
}