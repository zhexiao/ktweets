var eventSource = new EventSource("/tweets/stream");

eventSource.addEventListener('message', function(e) {
    string = e.data
    $('.tweets-wrap').prepend( string ) 
}, false);

eventSource.addEventListener('open', function(event) {
    console.log('----- Connection was opened -----');
}, false);

eventSource.addEventListener('error', function(event) {
    console.log('------ Connection was closed -----');
}, false);

