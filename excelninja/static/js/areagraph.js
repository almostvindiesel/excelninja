var is_editing_category = false

// Catch all Clicks
$(document).click(function() {
	var div_clicked_on = $(event.target);


	//Remove Edit Prompt and Save Category
	if (is_editing_category == true 
		&& div_clicked_on.attr('class') != 'twittercategory'
		&& div_clicked_on.attr('id') != 'twittercategorynew'
		) {
		is_editing_category = false;

		var new_category_text = $("#twittercategorynew").val(); 

		$("div.twittercategory").text(new_category_text);

	}

	// Create Prompt to Edit Category
	if (div_clicked_on.attr('class') == 'twittercategory' && is_editing_category == false) {
		var current_category_value = div_clicked_on.text()
		var input = '<input type="text" id="twittercategorynew" value="' +current_category_value + '">'
		$("div.twittercategory").html(input);
		is_editing_category = true;
	}

});


function display_data_table(data) {
	//console.log("length " + data[0]['values'].length);
	console.log(data[0]['values'][0][0]);

	//var topicSelected = data[0[]]

	 $('div.twittercategory').text(data[0]['key']);
	 var tweet_text = "";
	 var tweets = ['Enterway ethay Englishway exttay erehay atthay ouyay antway anslatedtray intoway',
	 		   'AvaScriptjay ogrampray. Otenay atthay yphenatedhay ordsway areway eatedtray a',
	 		   'andway away-zay. Allway unctuationpay, umera',
	 		   'Ethay outinesray areway ittenwray inway',
	 		   'Ethay algorithmsway ereway evelopedday andway'
	 		   ]

	tweets = shuffle(tweets);

	for (i = 0; i < tweets.length; i++) { 
	    tweet_text += tweets[i] + "<br>";
	    //console.log(data[0]['values'][i]);
	}

	 $('div.twitterdata').html(tweet_text);
	 /*
	 for (i = 0; i < data[0]['values'].length && i < 5; i++) { 
	    tweet_text += data[0]['values'][i][0] + "<br>";
	    //console.log(data[0]['values'][i]);
	 }
	 */
	 

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
