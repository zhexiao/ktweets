var eventSource = new EventSource("/tweets/stream");

eventSource.addEventListener('message', function(e) {
    console.log(message) 
}, false);

eventSource.addEventListener("date", function(e) {
    console.log(e.data)
});

eventSource.addEventListener('open', function(event) {
    console.log('----- Connection was opened -----');
}, false);

eventSource.addEventListener('error', function(event) {
    console.log('------ Connection was closed -----');
}, false);