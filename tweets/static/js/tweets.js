// var eventSource = new EventSource("/tweets/stream");
//
// eventSource.addEventListener('message', function(e) {
//     var res_html = e.data,
//         id = e.lastEventId;
//
//     $('.tweets-wrap').prepend( res_html )
//     $("#"+id).find('[data-toggle="tooltip"]').tooltip()
// }, false);
//
// eventSource.addEventListener('open', function(event) {
//     console.log('----- Connection was opened -----');
// }, false);
//
// eventSource.addEventListener('error', function(event) {
//     console.log('------ Connection was closed -----');
// }, false);



var remove_data = function(event){
    var $obj = $(event.target),
        id = $obj.attr('data-id');
}

var save_data = function(event){
    var $obj = $(event.target),
        $parent = $obj.closest('.ti-input-wrap'),
        name = $.trim( $parent.find('.ti-input').val() ),
        csrf = $parent.find('input[name="csrfmiddlewaretoken"]').val();


        data = {
            csrfmiddlewaretoken : csrf
        };

    if(name == ''){
        alert('Please enter a correct search data.');
        return;
    }

    data['name'] = name;
    data['type'] = '@';

    $.ajax({
        type : 'post',
        data : data,
        url : '/tweets/save_stream'
    }).done(function(){
        location.reload();
    })
}
