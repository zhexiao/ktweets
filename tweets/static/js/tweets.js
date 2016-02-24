var eventSource = new EventSource("/tweets/stream");

eventSource.addEventListener('message', function(e) {
    var res_html = e.data,
        id = e.lastEventId;

    $('.tweets-wrap').prepend( res_html )
    $("#"+id).find('[data-toggle="tooltip"]').tooltip()
}, false);

eventSource.addEventListener('open', function(event) {
    console.log('----- Connection was opened -----');
}, false);

eventSource.addEventListener('error', function(event) {
    console.log('------ Connection was closed -----');
}, false);



var remove_data = function(event){
    var $obj = $(event.target),
        $parent = $obj.closest('.tweets-init'),
        id = $obj.attr('data-id'),
        type = $obj.attr('data-type');

    var data = {
        csrfmiddlewaretoken : $parent.find('input[name="csrfmiddlewaretoken"]').val(),
        id : id,
        type : type
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
        name = $.trim( $parent.find('.ti-input').val() ),
        csrf = $parent.find('input[name="csrfmiddlewaretoken"]').val();


    var data = {
        csrfmiddlewaretoken : csrf
    };

    if(name == ''){
        alert('Please enter a correct search data.');
        return;
    }

    data['name'] = name;
    data['type'] = $obj.attr('data-type');

    $.ajax({
        type : 'post',
        data : data,
        url : '/tweets/save_stream'
    }).done(function(){
        location.reload();
    })
}
