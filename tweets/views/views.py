from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.conf import settings
from tweets.models import TwitterMention
from pprint import pprint

import ujson as json
import sys, os, redis, time, re, uuid

# error report message
def error_report(error_message):
    print(error_message)



# home page
@login_required
def index(request):
    mentions = request.user.tw_mention.all()

    return render(request, 'tweets/index.html', {
        'section' : 'index',
        'mentions' : mentions
    })


# stream data
@login_required
def stream_data(request):
    try:
        REDIS_CONF = {
            'host': settings.REDIS_DB_HOST,
            'port': settings.REDIS_PORT,
            'db': settings.REDIS_DB_NUMBER,
        }
        red = redis.StrictRedis(**REDIS_CONF)

        # get users mention data
        mentions = request.user.tw_mention.values_list('name', flat=True).order_by('name')
        # if exist mentions, get these data
        if mentions:
            mentions_with_tag = []
            for men in mentions:
                mentions_with_tag.append('@'+men)
        # if not exist mentions, tracking heartbeat(@@hb) to keep stream live
        else:
            mentions_with_tag = ['@@hb']


        # start initial pubsub
        pubsub = red.pubsub()
        # subscribe data
        pubsub.subscribe(mentions_with_tag)

        # listen published data
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
@login_required
def stream(request):
    return StreamingHttpResponse(stream_data(request), content_type="text/event-stream")



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



@login_required
def save_stream(request):
    if request.method == "POST":
        name = request.POST['name']
        type = request.POST['type']

        if type == '@':
            try:
                tm = TwitterMention.objects.get(name=name)
            except Exception as e:
                tm = TwitterMention(name=name)
                tm.save()


            # add this mention id xref to user
            current_user = request.user
            tm.user.add(current_user)

    return HttpResponse(1)


@login_required
def delete_stream(request):
    if request.method == "POST":
        id = request.POST['id']
        type = request.POST['type']

        if type == '@':
            try:
                tm = TwitterMention.objects.get(id=id)
                current_user = request.user
                tm.user.remove(current_user)
            except Exception as e:
                error_report(e)

    return HttpResponse(1)
