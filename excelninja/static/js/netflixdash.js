
function create_or_update_charts() {

    // ------------------------------------------------------------------------
    // Extract tokens for filtering dashboards

    //var selected_measures = []; //['Netflix','HBO'];
    var measures1 = [];
    var selected_measure1  = $(".measure-input1>option:selected").map(function() { 
      return $(this).val(); 
    });
    for (i = 0; i < selected_measure1.length; i++) {
      measures1[i] = selected_measure1[i];
    }
    console.log("selected_measure1");
    console.log(measures1);

    var measures2 = [];
    var selected_measure2  = $(".measure-input2>option:selected").map(function() { 
      return $(this).val(); 
    });
    for (i = 0; i < selected_measure2.length; i++) {
      measures2[i] = selected_measure2[i];
    }

    console.log("selected_measure2");
    console.log(measures2);



    /*
    var selected_countries = [];
    var countries = [];
    selected_countries  = $(".country-input>option:selected").map(function() { 
      return $(this).val(); 
    });
    for (i = 0; i < selected_countries.length; i++) {
      countries[i] = selected_countries[i];
    }
    */

    /*
    var selected_age_ranges = [];
    var age_ranges = [];
    selected_age_ranges = $(".age_range-input>option:selected").map(function() { 
      return $(this).val(); 
    });
    for (i = 0; i < selected_age_ranges.length; i++) {
      age_ranges[i] = selected_age_ranges[i];
    }
    
    var selected_genders = [];
    var genders = [];
    selected_genders   = $(".gender-input>option:selected").map(function() { 
      return $(this).val(); 
    });
    for (i = 0; i < selected_genders.length; i++) {
      genders[i] = selected_genders[i];
    }
    */


    // ------------------------------------------------------------------------
    // Hit API Endpoints to get json to generate dashboards

    $.post("/netflix/api/country.json", { 
      
        measure1: measures1[0],
        measure2: measures2[0]
      },
      function(data) {
        create_country_chart(data);
      }
    );

    /*
    $.post("/daudash/api/countrypenetration.json", { 
        age_ranges: JSON.stringify(age_ranges),
        countries: JSON.stringify(countries),
        genders: JSON.stringify(genders)
      },
      function(data) {
        create_country_penetration_chart(data);
      }
    );
    */

    $.post("/netflix/api/agepct.json", { 
        measure1: measures1[0],
        measure2: measures2[0]
      },
      function(data) {
        create_age_pct_chart(data);
      }
    );

    
    $.post("/netflix/api/genderpct.json", { 
        measure: measures1[0],
      },
      function(data) {
        create_gender_pct_chart(data, 'measure1');
      }
    );

    $.post("/netflix/api/genderpct.json", { 
        measure: measures2[0],
      },
      function(data) {
        create_gender_pct_chart(data, 'measure2');
      }
    );
    
}

// Global Chart Defaults
Chart.defaults.global.tooltips = false;
Chart.defaults.global.responsive = true;
Chart.defaults.global.defaultFontColor = 'black';
Chart.defaults.global.legend.display = false;
Chart.defaults.global.maintainAspectRatio = false;  

var MinGraphHeight = 50;
var PixelHeightPerDatum = 50;

// ------------------------------------------------------------------------
// The following functions generate charts for each section
// Reference: http://stackoverflow.com/questions/31631354/how-to-display-data-values-on-chart-js

function create_country_chart(json) {

  document.getElementById("country").setAttribute("height", MinGraphHeight + PixelHeightPerDatum * json.datasets[0].data.length);
  document.getElementById("chartcol1").style.maxHeight = MinGraphHeight + PixelHeightPerDatum * json.datasets[0].data.length + 'px';


  var options = {
    /*barWidth:20,
    isFixedWidth:false,*/
    scales: {
      xAxes: [{
          gridLines: {
              color: "rgba(0, 0, 0, 0)",
          },
          afterBuildTicks: function(myChart) {    
            myChart.ticks = [];
          }
      }],
      yAxes: [{
          barThickness: 20,
          gridLines: {
              color: "rgba(0, 0, 0, 0)",
          } 
      }]
    },
    events: false,
    tooltips: {
        enabled: false
    },
    hover: {
        animationDuration: 0
    },
    animation: {
        duration: 1,
        onComplete: function () {
            var chartInstance = this.chart,
                ctx = chartInstance.ctx;
            ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
            ctx.textAlign = 'center';
            ctx.textBaseline = 'bottom';
            ctx.fillStyle = 'black';

            this.data.datasets.forEach(function (dataset, i) {
                var meta = chartInstance.controller.getDatasetMeta(i);
                meta.data.forEach(function (bar, index) {
                    var data = dataset.data[index];                            
                    ctx.fillText(data.toLocaleString(), bar._model.x + 32, bar._model.y + 8);
                });
            });
        }
    }
  }

  var ctx = document.getElementById("country").getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: json,
    options
  });
}

/*
function create_country_penetration_chart(json) {
 
  document.getElementById("countrypenetration").setAttribute("height", MinGraphHeight + PixelHeightPerDatum * json.datasets[0].data.length);
  document.getElementById("chartcol2").style.maxHeight = MinGraphHeight + PixelHeightPerDatum * json.datasets[0].data.length + 'px';

  var options = {
    showTooltips: false,
    scales: {
      xAxes: [{
          gridLines: {
              color: "rgba(0, 0, 0, 0)",
          },
          afterBuildTicks: function(myChart) {    
            myChart.ticks = [];
          }
      }],
      yAxes: [{
          barThickness: 20,
          //barValueSpacing: 3,
          gridLines: {
              color: "rgba(0, 0, 0, 0)",
          } 
      }]
    },
    events: false,
    tooltips: {
        enabled: false
    },
    hover: {
        animationDuration: 0
    },
    animation: {
        duration: 1,
        onComplete: function () {
            var chartInstance = this.chart,
                ctx = chartInstance.ctx;
            ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
            ctx.textAlign = 'center';
            ctx.textBaseline = 'bottom';
            ctx.fillStyle = 'black';

            this.data.datasets.forEach(function (dataset, i) {
                var meta = chartInstance.controller.getDatasetMeta(i);
                meta.data.forEach(function (bar, index) {
                    var data = dataset.data[index] + '%';                            
                    ctx.fillText(data, bar._model.x + 20, bar._model.y + 8);
                });
            });
        }
    }
  }

  var ctx = document.getElementById("countrypenetration").getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: json,
    options
  });
}
*/


function create_age_pct_chart(json) {

  document.getElementById("agepct").setAttribute("height",  MinGraphHeight + PixelHeightPerDatum * json.datasets[0].data.length);
  document.getElementById("chartcol3").style.maxHeight = MinGraphHeight + PixelHeightPerDatum * json.datasets[0].data.length + 'px';


  var options = {
    showTooltips: false,
    scales: {
      xAxes: [{
          gridLines: {
              color: "rgba(0, 0, 0, 0)",
          },
          afterBuildTicks: function(myChart) {    
            myChart.ticks = [];
          }
      }],
      yAxes: [{
          barThickness: 20,
          gridLines: {
              color: "rgba(0, 0, 0, 0)",
          } 
      }]
    },
    events: false,
    tooltips: {
        enabled: false
    },
    hover: {
        animationDuration: 0
    },
    animation: {
        duration: 1,
        onComplete: function () {
            var chartInstance = this.chart,
                ctx = chartInstance.ctx;
            ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
            ctx.textAlign = 'center';
            ctx.textBaseline = 'bottom';
            ctx.fillStyle = 'black';

            this.data.datasets.forEach(function (dataset, i) {
                var meta = chartInstance.controller.getDatasetMeta(i);
                meta.data.forEach(function (bar, index) {
                    var data = dataset.data[index] + '%';                            
                    ctx.fillText(data, bar._model.x + 20, bar._model.y + 8);
                });
            });
        }
    }
  }
  var ctx = document.getElementById("agepct").getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: json,
    options
  });
}



function create_gender_pct_chart(json, measure) {

  var PixelHeightPerDatum = 30;

  document.getElementById("genderpct" + measure).setAttribute("height",  + PixelHeightPerDatum * json.datasets[0].data.length);
  document.getElementById("chartcol4" + measure).style.maxHeight = '200px';

  function generate_legend() {
    labels = json['labels'];
    values =  json['datasets'][0]['data'];
    bgColors = json['datasets'][0]['backgroundColor']
    var legendHtml = '';
    for (i = 0; i < labels.length; i++) { 
      legendHtml += '<span style="background-color:'+bgColors[i]+';">&nbsp;&nbsp&nbsp;&nbsp;&nbsp;</span> ' + labels[i] + ' (' + values[i] + '%) '
    }
    document.getElementById("genderlegend" + measure).innerHTML = legendHtml;
  }


  var options = {
    //cutoutPercentage: 10,
    legend: {
      display : false,
    },
    events: false,
    showAllTooltips: true,
    hover: {
        animationDuration: 0
    },
    animation: {
        duration: 1,
        onComplete: function () {
            var chartInstance = this.chart,
                ctx = chartInstance.ctx;
            ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
            ctx.textAlign = 'center';
            ctx.textBaseline = 'bottom';
            ctx.fillStyle = 'black';

            generate_legend();
        }
    }
  }

  var ctx = document.getElementById("genderpct" + measure).getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'pie',
    data: json,
    options  
  });
}


