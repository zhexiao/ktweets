var eventSource = new EventSource("/tweets/stream");
var tweets_html_source   = $("#entry-template").html();
var tweets_template = Handlebars.compile(tweets_html_source);

eventSource.addEventListener('message', function(e) {
    var output = e.data.slice(2, -1).replace(/[\\]/g, '');
    console.log(JSON.parse(JSON.stringify(output)))
    var string = tweets_template(JSON.parse(JSON.stringify(output)));   
    $('.cf-wrap').append(string + '<br><br><br>') 
}, false);

eventSource.addEventListener('open', function(event) {
    console.log('----- Connection was opened -----');
}, false);

eventSource.addEventListener('error', function(event) {
    console.log('------ Connection was closed -----');
}, false);

