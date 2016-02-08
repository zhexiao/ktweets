from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import cache
import redis



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
        yield "data: %s\n\n" % (message)



def stream(request):
    response = HttpResponse(stream_data(), content_type="text/event-stream")
    cache.add_never_cache_headers(response)
    return response