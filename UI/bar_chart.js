$(document).ready(function() {  
   var chart = {
      type: 'bar'
   };
   var title = {
      text: 'Tweet Computation'   
   };
   var subtitle = {
      text: 'Source: https://www.twitter.com/'  
   };
   var xAxis = {
      categories: ['Jan', 'Feb', 'Mar', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      title: {
         text: null
      }
   };
   var yAxis = {
      min: 0,
      title: {
         text: 'Sentiment',
         align: 'high'
      },
      labels: {
         overflow: 'justify'
      }
   };
   var tooltip = {
      valueSuffix: ' millions'
   };
   var plotOptions = {
      bar: {
         dataLabels: {
            enabled: true
         }
      }
   };
   var legend = {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'top',
      x: -40,
      y: 100,
      floating: true,
      borderWidth: 1,
      backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
      shadow: true
   };
   var credits = {
      enabled: false
   };
   
   var series= [{
         name: 'Positivity',
            data: [1107, 301, 635, 203, 280, 488, 739, 890, 1689, 1459]
        }, {
            name: 'Negativity',
            data: [973, 914, 205, 732, 34, 49, 1746, 1233, 1027, 867]      
	    }
   ];     
      
   var json = {};   
   json.chart = chart; 
   json.title = title;   
   json.subtitle = subtitle; 
   json.tooltip = tooltip;
   json.xAxis = xAxis;
   json.yAxis = yAxis;  
   json.series = series;
   json.plotOptions = plotOptions;
   json.legend = legend;
   json.credits = credits;
   $('#container_bar_chart').highcharts(json);
  
});