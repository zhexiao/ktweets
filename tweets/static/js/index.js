var eventSource = new EventSource("/tweets/stream");

eventSource.addEventListener('message', function(e) {
    string = e.data
    $('.cf-wrap').prepend( string + '<br><br><br>') 
}, false);

eventSource.addEventListener('open', function(event) {
    console.log('----- Connection was opened -----');
}, false);

eventSource.addEventListener('error', function(event) {
    console.log('------ Connection was closed -----');
}, false);

