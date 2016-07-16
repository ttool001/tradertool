$(document).ready(function() { 

      function addInitialValues(pos_values, neg_values){
         chartData = {}

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
            categories: ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'],
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
            x: 10,
            y: 0,
            floating: true,
            borderWidth: 1,
            backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
            shadow: true
         };
         var credits = {
            enabled: false
         };

         var series = [{name:'Positivity',data:pos_values}, {name:'Negativity', data:neg_values}]

         chartData.chart = chart; 
         chartData.title = title;   
         chartData.subtitle = subtitle; 
         chartData.xAxis = xAxis;
         chartData.yAxis = yAxis;  
         chartData.series = series;
         chartData.plotOptions = plotOptions;
         chartData.legend = legend;
         chartData.credits = credits;
         return chartData;

      }

$('#search_button').click(function(){
      var endpoint = 'http://python-jphackathon.rhcloud.com/getticker/';
      var nameOfTicker = $("#search").val();
      var fullendpoint = endpoint + nameOfTicker;


      if (nameOfTicker == '') {
         chartData = {title:{text:"No Ticker Entered"}};
         $('#container_bar_chart').highcharts(chartData);
      } else {
         $.get(fullendpoint, function(result){
            dayDict = {'Mon':0, 'Tue':1, 'Wed':2, 'Thurs':3, 'Thur':3, 'Thu':3, 'Fri':4, 'Sat':5, 'Sun':6 }
            pos_values = [0,0,0,0,0,0,0];
            neg_values = [0,0,0,0,0,0,0];
            if (result.length > 0){
               for (var i = 0; i < result.length; i++){
                  day =  result[i]['date'].split(' ')[0];
                  pos_values[dayDict[day]] = result[i]["tpc"];
                  neg_values[dayDict[day]] = result[i]["tnc"];
               }

            } else{
               chartData = {title:{text:"Ticker Doesn't Exist"}};
               $('#container_bar_chart').highcharts(chartData);
            }
            chartData = addInitialValues(pos_values, neg_values);
            $('#container_bar_chart').highcharts(chartData);
         });
      }
      
   });


  
});