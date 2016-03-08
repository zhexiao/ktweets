var eventSource = new EventSource("/tweets/stream"),
    tweets_wrap = $('.tweets-wrap');

// listen message event
eventSource.addEventListener('message', function(e) {
    var res_html = e.data,
        id = e.lastEventId;

    // $('.tweets-wrap').prepend( res_html )

    // append new data into page
    tweets_wrap.waterfall('prepend', res_html, function(){
        $("#"+id).find('[data-toggle="tooltip"]').tooltip();
        $("#"+id).addClass('show-tweet');

        // if the tweets more than 100, then remove the rest of tweets
        var tweets_length = tweets_wrap.find('.tt-wrap').length;
        if(tweets_length > 60){
            tweets_wrap.find('.tt-wrap').last().remove();
        }
    });
}, false);

// listen event open function
eventSource.addEventListener('open', function(event) {
    tweets_wrap.waterfall({
    	itemCls: 'tt-wrap',
    	fitWidth: true,
    	colWidth: 340,
        gutterHeight : 50,
        checkImagesLoaded : false,
        loadingMsg : false
    });

    console.log('----- Connection was opened -----');
}, false);

// listen event close function
eventSource.addEventListener('error', function(event) {
    console.log('------ Connection was closed -----');
}, false);



var remove_data = function(event){
    var $obj = $(event.target),
        $parent = $obj.closest('.tweets-init'),
        id = $obj.attr('data-id');

    var data = {
        csrfmiddlewaretoken : $parent.find('input[name="csrfmiddlewaretoken"]').val(),
        id : id
    };

    $.ajax({
        type : 'post',
        data : data,
        url : '/tweets/delete_stream'
    }).done(function(){
        location.reload();
    })
}

var save_data = function(event){
    var $obj = $(event.target),
        $parent = $obj.closest('.ti-input-wrap'),
        text = $.trim( $parent.find('.ti-input').val() ),
        csrf = $parent.find('input[name="csrfmiddlewaretoken"]').val();


    var data = {
        csrfmiddlewaretoken : csrf
    };

    if(text == ''){
        alert('Please enter a correct search data.');
        return;
    }

    data['text'] = text;

    $.ajax({
        type : 'post',
        data : data,
        url : '/tweets/save_stream'
    }).done(function(){
        location.reload();
    })
}
