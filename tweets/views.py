from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.template.loader import get_template
import ujson as json
import sys, os, redis, time, re, uuid

# error report message
def error_report(error_message):
    print(error_message)

# home page
def index(request):
    return render(request, 'tweets/index.html')       

# stream data
def stream_data():
    try:
        REDIS_CONF = {
            'host': 'localhost',
            'port': 6379,
            'db': 1,
        }
        red = redis.StrictRedis(**REDIS_CONF)

        pubsub = red.pubsub()
        pubsub.subscribe(['@NBA', '@zhexiao27'])

        for message in pubsub.listen():
            uniqid_id = str(uuid.uuid4())
            data = stream_parse(message['data'], uniqid_id)

            if data != '':
                yield "id: %s\n\n" % uniqid_id
                yield "data: %s\n\n" % data
                time.sleep(1)
    except Exception as e:
        error_report(e)

# stream handle
def stream(request):
    return StreamingHttpResponse(stream_data(), content_type="text/event-stream")


# check the data image and video
def stream_data_media_check(data):
    media = {}
    try:
        if 'extended_entities' in data:
            if 'media' in data['extended_entities']:
                media['id_str'] = data['extended_entities']['media'][0]['id_str']
                media['image_url'] = data['extended_entities']['media'][0]['media_url']
                media['link_url'] = data['extended_entities']['media'][0]['url']
                media['type'] = data['extended_entities']['media'][0]['type']
    except Exception as e:
        error_report(e)

    return media


# convert plain text to a clickable link
def stream_text_convert_to_url(text):
    pass


# filter stream data and return html
def stream_parse(data, uniqid_id):
    html = ''

    try:
        json_obj = json.loads(data)

        media = stream_data_media_check(json_obj)

        html = get_template('tweets/tweets_tpl.html').render({
            'uniqid_id' : uniqid_id,
            'text': json_obj['text'],
            'name' : json_obj['user']['name'],
            'screen_name' : json_obj['user']['screen_name'],
            'profile_image' : json_obj['user']['profile_image_url'],
            'created_at' : json_obj['created_at'],
            'media' : media,
            'url' : 'https://twitter.com/%s/status/%s' % (json_obj['user']['screen_name'], json_obj['id_str'])
        }) 
        
        # remove \n and \r
        html = html.replace('\n', ' ').replace('\r', '')
    except Exception as e:
        error_report(e) 
   
    return html

