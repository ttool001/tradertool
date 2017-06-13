$(document).ready(function() {

   function addInitialValues(pos_values, neg_values){
      var chartData = {}
      var title = {
         text: 'Average Tweet Sentiment'   
      };
      var subtitle = {
         text: 'Source: https://www.twitter.com/'
      };
      var xAxis = {
         categories: ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat','Sun']
      };

      var yAxis = { title: {text: 'Sentiment'}, plotLines: [{value: 0,width: 1,color: '#808080'}]};  



      var legend = {
         layout: 'vertical',
         align: 'right',
         verticalAlign: 'middle',
         borderWidth: 0
      };

      var series = [{name:'Positivity',data:pos_values}, {name:'Negativity', data:neg_values}]

      chartData.title = title;
      chartData.subtitle = subtitle;
      chartData.xAxis = xAxis;
      chartData.yAxis = yAxis;
      // chartData.tooltip = tooltip;
      chartData.legend = legend;
      chartData.series = series;
      return chartData;

   }


   $('#search_button').click(function(){
      var endpoint = 'http://mldemo-dushen1.rhcloud.com/getticker/';
      var nameOfTicker = $("#search").val();
      var fullendpoint = endpoint + nameOfTicker;


      if (nameOfTicker == '') {
         chartData = {title:{text:"No Ticker Entered"}};
         $('#container_line_chart').highcharts(chartData);

      } else {
         $.get(fullendpoint, function(result){
            dayDict = {'Mon':0, 'Tue':1, 'Wed':2, 'Thu':3, 'Fri':4, 'Sat':5, 'Sun':6 }
            pos_values = [0,0,0,0,0,0,0];
            neg_values = [0,0,0,0,0,0,0];
            if (!$.isEmptyObject(result)){
               for (var i = 0; i < result.length; i++){
                  day =  result[i]['date'].split(' ')[0];
                  pos_values[dayDict[day]] = result[i]["tps"];
                  neg_values[dayDict[day]] = result[i]["tns"];
                  chartData = addInitialValues(pos_values, neg_values);
                  $('#container_line_chart').highcharts(chartData);
               }

            } else{
               chartData = {title:{text:"Ticker Doesn't Exist"}};
               $('#container_line_chart').highcharts(chartData);
            }
         });
      }
      
   });


});
