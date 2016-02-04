from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import redis



def index(request):
    return render(request, 'tweets/index.html')       




def stream(request):
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
            long_string = '''
            id: 123 \n\n
            data: 123123123 \n
            '''
            return long_string

    return HttpResponse(stream_data(), content_type="text/event-stream")