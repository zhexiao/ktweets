from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.template.loader import get_template
import ujson as json
import redis, time


def index(request):
    return render(request, 'tweets/index.html')       


def stream_data():
    REDIS_CONF = {
        'host': 'localhost',
        'port': 6379,
        'db': 1,
    }
    red = redis.StrictRedis(**REDIS_CONF)

    pubsub = red.pubsub()
    pubsub.subscribe('@NBA')

    for message in pubsub.listen():
        data = stream_parse(message['data'])

        yield "id: %s\n\n" % 1
        yield "data: %s\n\n" % data
        time.sleep(1)


def stream(request):
    return StreamingHttpResponse(stream_data(), content_type="text/event-stream")


def stream_parse(data):
    html = ''

    try:
        json_obj = json.loads(data)
        html = get_template('tweets/tweets_tpl.html').render({
            'text': json_obj['text'],
            'name' : json_obj['user']['name'],
            'screen_name' : json_obj['user']['screen_name'],
            'profile_image' : json_obj['user']['profile_image_url']
        }) 
        
        # remove \n and \r
        html = html.replace('\n', ' ').replace('\r', '')
    except Exception as e:
        print(e) 
   
    return html