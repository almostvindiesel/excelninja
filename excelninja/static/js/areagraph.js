var is_editing_category = false

// Catch all Clicks
$(document).click(function() {
	var div_clicked_on = $(event.target);


	//Remove Edit Prompt and Save Category
	if (is_editing_category == true 
		&& div_clicked_on.attr('class') != 'topiccategory'
		&& div_clicked_on.attr('id') != 'topiccategorynew'
		) {
		is_editing_category = false;

		var new_category_text = $("#topiccategorynew").val(); 

		$("div.topiccategory").text(new_category_text);

	}

	// Create Prompt to Edit Category
	if (div_clicked_on.attr('class') == 'topiccategory' && is_editing_category == false) {
		var current_category_value = div_clicked_on.text()
		var input = '<input type="text" id="topiccategorynew" value="' +current_category_value + '">'
		$("div.topiccategory").html(input);
		is_editing_category = true;
	}

});


function display_tweets(current_topic_key) {
	

	// Change html to show current topic
	$('div.topiccategory').text(current_topic_key);

	//Change tweets displayed based on current topic
	var tweet_html = "<ol>";
	var added_tweets = 0;
	var max_tweets_to_show = 8;
	for (i = 0; i < tweets_from_topics.length && added_tweets < max_tweets_to_show; i++) { 
		if(tweets_from_topics[i]['topic'] == current_topic_key) {
		    tweet_html += "<li>" + tweets_from_topics[i]['tweet'] + "</li><br>";
		    added_tweets = added_tweets + 1;
	    }
	 }
	 tweet_html = tweet_html+"</ol>"
	 $('div.tweets').html(tweet_html);

}

function display_hashtags(current_topic_key) {
	
	//Change tweets displayed based on current topic
	var hashtag_html = "<ol>";
	var added_hashtags = 0;
	var max_hashtags_to_show = 8;
	for (i = 0; i < hashtags_from_topics.length && added_hashtags < max_hashtags_to_show; i++) { 
		if(hashtags_from_topics[i]['topid_id'] == current_topic_key) {
			if ( !hashtags_from_topics[i]['hashtag'].includes("houseof") ) { 
				hashtag_html += "<li>" + hashtags_from_topics[i]['hashtag'] + "</li><br>";
		    	added_hashtags = added_hashtags + 1;
			}
	    }
	 }
	 hashtag_html = hashtag_html+"</ol>"
	 $('div.hashtags').html(hashtag_html);
	 
}

function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}
