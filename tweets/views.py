from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
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
        yield 'id: %s\n\n' % 1
        yield 'data: %s\n\n' % message['data']
        time.sleep(1)


def stream(request):
    return StreamingHttpResponse(stream_data(), content_type="text/event-stream")