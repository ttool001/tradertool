$(document).ready(function(){
	$('#myModal').on('shown.bs.modal', function(){
		// console.log($('#search').val());
		var endpoint = 'http://python-jphackathon.rhcloud.com/get_sample_tweets/';
		var stock_name = $('#search').val();

		var fullendpoint = endpoint + stock_name;
		$.get(endpoint, function(result){
			console.log(result);
			pos_tweets = result['pos_tweets']
			neg_tweets = result['neg_tweets']
		});
	});


});

