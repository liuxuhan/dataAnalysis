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
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            document.getElementById('priceSpan').innerHTML = data['price'];
            $("div.price").removeClass('hidden');
            showGaugeChart(data);
            // getCluster(param)
            console.log(this.responseText);
        }
    };
    xhttp.open("POST", "http://127.0.0.1:5002/predict", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify(param));
}

function getCluster(param) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
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
    d3.csv(fileName, function(error, data) {
        data.forEach(function(d) {
            d.value = +d.value;
        });
        chart1 = makeDistroChart({
            data: data,
            xName: 'date',
            yName: 'value',
            axisLabels: {
                xAxis: null,
                yAxis: 'Prices'
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

function showPage(self, pageName) {
    $("a.nav-link").removeClass('active');
    $(self).addClass("active");
    className = "div." + pageName + "Page";
    $('div.pages').addClass("hidden");
    $(className).removeClass("hidden");
    // if (pageName == 'visual' && $("div.chart-wrapper").children().length == 0) {
    //     creatChart('data.csv');
    // }
}

function validate() {
    if ($("input#inputKm")[0].value != "" && $("input#inputYear")[0].value != "") {
        document.getElementById("searchBtn").disabled = false;
    } else {
        document.getElementById("searchBtn").disabled = true;
    }
}

var stateData;
var amountData;
var boxplotData;
var yearData;

function displayStateData(data) {
    var name = data['name'].split("<br/>")[0];
    for (i = 0; i < stateData.length; i++) {
        state = stateData[i];
        if (state['StateName'] == name) {
            createPanelforMap(state);
            break;
        }
    }
}

function createPanelforMap(data) {
    var panelString = "<li class='list-group-item list-group-item-primary'><b>" + data['StateName'] + "</b></li>";
    panelString += "<li class='list-group-item list-group-item-info'><b><i>Car Price</i></b></li>";
    panelString += "<li class='list-group-item'>Max: ₹" + data['max_price'] + "</li>";
    panelString += "<li class='list-group-item'>Average: ₹" + parseInt(data['avg_price']) + "</li>";
    panelString += "<li class='list-group-item'>Minimum: ₹" + data['min_price'] + "</li>";
    panelString += "<li class='list-group-item list-group-item-info'><b><i>Bought Year</i></b></li>";
    panelString += "<li class='list-group-item'>Maximum: " + data['max_year'] + "</li>";
    panelString += "<li class='list-group-item'>Average: " + parseInt(data['avg_year']) + "</li>";
    panelString += "<li class='list-group-item'>Minimum: " + data['min_year'] + "</li>";
    panelString += "<li class='list-group-item list-group-item-info'><b><i>Mile Age (KM)</i></b></li>";
    panelString += "<li class='list-group-item'>Maximum: " + data['max_km'] + "</li>";
    panelString += "<li class='list-group-item'>Average: " + parseInt(data['avg_km']) + "</li>";
    panelString += "<li class='list-group-item'>Minimum: " + data['min_km'] + "</li>";
    $("ul#map-pannel-list-group").html(panelString);
}

$(function() {
    // send ajax request
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // console.log(this.responseText);
            stateData = JSON.parse(this.responseText);
            console.log("receive map data");
            // showGaugeChart(stateData);
        }
    };
    xhttp.open("GET", "http://127.0.0.1:5002/getmapdata", true);
    xhttp.send();

    var xhttp1 = new XMLHttpRequest();
    xhttp1.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // console.log(this.responseText);
            amountData = JSON.parse(this.responseText);
            console.log("receive amount data");
            showBoxPlot();
        }
    };
    xhttp1.open("GET", "http://127.0.0.1:5002/getamountdata", true);
    xhttp1.send();

    var xhttp2 = new XMLHttpRequest();
    xhttp2.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // console.log(this.responseText);
            boxplotData = JSON.parse(this.responseText);
            showBoxPlot();
        }
    };
    xhttp2.open("GET", "http://127.0.0.1:5002/getboxplotdata", true);
    xhttp2.send();

    var xhttp3 = new XMLHttpRequest();
    xhttp3.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // console.log(this.responseText);
            yearData = JSON.parse(this.responseText);
            showChartByYear();
        }
    };
    xhttp3.open("GET", "http://127.0.0.1:5002/getdatabyyear", true);
    xhttp3.send();
})

function showGaugeChart(data) {
    var myChart = echarts.init(document.getElementById('gaugeChart'));
    var option = {
        tooltip: {
            formatter: "{a} <br/>₹{c}"
        },
        toolbox: {
            feature: {
                restore: {},
                saveAsImage: {}
            }
        },
        series: [{
            name: 'Predicted Price',
            type: 'gauge',
            detail: { formatter: '₹{value}' },
            data: [{ value: data['price'] }],
            max: data['max'],
            min: data['min'],
            animationEasing: 'elasticOut',
            animationDuration: 4000,
            animation: true,
            splitLine: {
                length: 45,
                lineStyle: {
                    color: 'auto'
                }
            }
        }]
    };
    myChart.setOption(option);
}


function showBoxPlot() {
    if (!amountData || !boxplotData) {
        return
    }
    var barData = [];
    for (var i = 0; i < amountData.length; i++) {
        barData.push(amountData[i]['count'])
    }

    var seriesData = [];
    for (var j = 0; j < boxplotData.length; j++) {
        seriesData.push(boxplotData[j]['PriceList'].split(',').map(Number));
    }

    var data = dataTool.prepareBoxplotData(seriesData);

    for (var i = 0; i < data.axisData.length; i++) {
        data.axisData[i] = boxplotData[i].CarName;
    }

    option = {
        title: {
            text: 'Price Chart for Car Models of Toyota',
            subtext: '(Models is not listed if total amount is less than 10)',
            left: 'center',
            top: '50px'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '15%',
            top: '20%',
            right: '10%',
            bottom: '15%'
        },
        xAxis: {
            type: 'category',
            data: data.axisData,
            boundaryGap: true,
            nameGap: 30,
            axisLabel: {
                formatter: '{value}',
                rotate: 20
            }
        },
        yAxis: [{
            type: 'value',
            name: 'Price',
            min: 0,
            max: 6000000,
            position: 'left',
            splitArea: {
                show: false
            },
            splitNumber: 8,
            axisLine: {
                lineStyle: {
                    color: '#5793f3'
                }
            },
            axisLabel: {
                formatter: '₹{value}'
            }
        }, {
            type: 'value',
            name: 'Amount',
            min: 0,
            max: 300,
            splitNumber: 5,
            position: 'right',
            axisLine: {
                lineStyle: {
                    color: '#d14a61'
                }
            },
        }],
        dataZoom: [{
                type: 'inside',
                start: 0,
                end: 20
            },
            {
                show: true,
                height: 20,
                type: 'slider',
                top: '90%',
                xAxisIndex: [0],
                start: 0,
                end: 20
            }
        ],
        series: [{
            name: 'price',
            type: 'boxplot',
            itemStyle: {
                normal: {
                    borderColor: '#5793f3'
                }
            },
            data: data.boxData,
            tooltip: { formatter: formatter }
        }, {
            name: 'amount',
            type: 'bar',
            yAxisIndex: 1,
            itemStyle: {
                normal: {
                    opacity: 0.5
                }
            },
            data: barData
        }]
    };

    function formatter(param) {
        return [
            'Car Model: ' + param.name,
            'upper: ₹' + param.data[01] + 'L',
            'Q1: ₹' + param.data[2] + 'L',
            'median: ₹' + param.data[3] + 'L',
            'Q3: ₹' + param.data[4] + 'L',
            'lower: ₹' + param.data[5] + 'L'
        ].join('<br/>')
    }

    var myChart = echarts.init(document.getElementById('chart-distro1'));
    myChart.setOption(option);
    style = {
        "width": "750px",
        "height": "600px"
    }
    myChart.resize(style);
}


function showChartByYear() {
  var axisData_ = [];
  var barData_ = [];
  var lineData_ = [];
    for (var i = 0;i<yearData.length;i++){
      var thisYear = yearData[i];
      axisData_.push(thisYear.MakeYear);
      barData_.push(thisYear.amount);
      var pricelist = thisYear.PriceList.split(",").map(Number);
      var middleIndex = Math.floor(pricelist.length/2);
      lineData_.push(pricelist[middleIndex]);
    }
        option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross',
                    crossStyle: {
                        color: '#999'
                    }
                }
            },
            legend: {
                data: ['Amount', 'Median Price']
            },
            xAxis: [{
                type: 'category',
                data: axisData_,
                axisPointer: {
                    type: 'shadow'
                }
            }],
            yAxis: [{
                    type: 'value',
                    name: 'Amount',
                    min: 0,
                    max: 600,
                    interval: 50,
                    axisLabel: {
                        formatter: '{value}'
                    }
                },
                {
                    type: 'value',
                    name: 'Price',
                    min: 0,
                    max: 5000000,
                    splitNumber: 10,
                    axisLabel: {
                        formatter: '₹ {value}'
                    }
                }
            ],
            series: [{
                    name: 'Amount',
                    type: 'bar',
                    itemStyle: {
                        normal: {
                            color: "#4db8ff"
                        }
                    },
                    data: barData_
                },
                {
                    name: 'Median Price',
                    type: 'line',
                    yAxisIndex: 1,
                    data: lineData_
                }
            ]
        };
    var myChart = echarts.init(document.getElementById('chart-year'));
    myChart.setOption(option);
    style = {
        "width": "750px",
        "height": "600px"
    }
    myChart.resize(style);

}