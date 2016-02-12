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


