$(document).ready(function(){
	$('#myModal').on('shown.bs.modal', function(){
		$('#twitters_list').empty();
		// console.log($('#search').val());
		var table_row_head = '<div class="row">';
		var table_footer = '</div>';
		var table_col_head = '<div class="col-sm-6">';
		var table_offset = '<div class="col-sm-offset-6">'
		var p = '<p>'
		var endp = '</p>' 


		var endpoint = 'http://python-jphackathon.rhcloud.com/get_sample_tweets/';
		var stock_name = $('#selected_ticker').text();
		var fullendpoint = endpoint + stock_name;
		console.log(fullendpoint);
		rows = '';
		$.get(fullendpoint, function(result){
			console.log(result);
			pos_tweets = result['pos_list']
			neg_tweets = result['neg_list']
			console.log(pos_tweets)
			console.log(neg_tweets)

			if(pos_tweets.length < neg_tweets.length){
				for (var i = 0; i < pos_tweets.length; i++){
					row = table_row_head + table_col_head + p + pos_tweets[i] + endp + table_footer + table_offset + p + neg_tweets[i] + endp + table_footer + table_footer;
					//console.log(row);
					rows += row;
				} 

				for (var i = pos_tweets.length; i < neg_tweets.length; i++){
					row = table_row_head + table_col_head + p + neg_tweets[i] + endp + table_footer + table_footer;
					rows += row;
				}

			} else if(neg_tweets.length < pos_tweets.length){
				for (var i = 0; i < neg_tweets.length; i++){
					row = table_row_head + table_col_head + p + pos_tweets[i] + endp + table_footer + table_offset + p + neg_tweets[i] + endp + table_footer + table_footer;
					rows += row;
				} 

				for (var i = neg_tweets.length; i < pos_tweets.length; i++){
					row = table_row_head + table_col_head + p + pos_tweets[i] + endp + table_footer + table_footer;
					rows += row;
				}

			} else {

				for (var i = 0; i < pos_tweets.length; i++){
					
					row = table_row_head + table_col_head + p + pos_tweets[i] + endp + table_footer + table_offset + p + neg_tweets[i] + endp + table_footer + table_footer;
					rows += row;
					console.log(row);
				}

			}

			$('#twitters_list').append(rows);
		});
	});


});

