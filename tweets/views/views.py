from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.conf import settings
from tweets.models import TwitterTracks
from pprint import pprint

import ujson as json
import sys, os, redis, time, re, uuid

# error report message
def error_report(error_message):
    print(error_message)


def get_ip(request):
    http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if http_x_forwarded_for:
        ip_address = http_x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    return ip_address


# home page
@login_required
def index(request):
    tw_tracks = request.user.tw_tracks.all()

    return render(request, 'tweets/index.html', {
        'section' : 'index',
        'tw_tracks' : tw_tracks
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

        # get users tracks data
        tw_tracks = request.user.tw_tracks.values_list('text', flat=True).order_by('text')

        # make tracks as a list
        tw_tracks_lists = []
        if tw_tracks:
            for t_t in tw_tracks:
                tw_tracks_lists.append(t_t)

        # add a heartbeat track to make connection alive
        tw_tracks_lists.append('__hb__')

        # start initial pubsub
        pubsub = red.pubsub()

        # publish a connection killer signal, uniqid id is user ip address
        kill_signal_data =  ('{0}_{1}').format('ip', str(get_ip(request)))
        red.publish('__clear__', kill_signal_data)

        # subscribe all data include the killer as well
        tw_tracks_lists.append('__clear__')
        pubsub.subscribe(tw_tracks_lists)

        # listen published data
        for message in pubsub.listen():
            uniqid_id = str(uuid.uuid4())
            # if the channel is killer, start clear dead connection
            if message['channel'].decode('utf-8') == '__clear__':
                try:
                    if message['data'].decode('utf-8') == kill_signal_data:
                        pubsub.unsubscribe()
                        break
                except Exception as e:
                    pass
            else:
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
        text = request.POST['text']

        try:
            tt = TwitterTracks.objects.get(text=text)
        except Exception as e:
            tt = TwitterTracks(text=text)
            tt.save()


        # add this track id xref to user
        current_user = request.user
        tt.user.add(current_user)

    return HttpResponse(1)


@login_required
def delete_stream(request):
    if request.method == "POST":
        id = request.POST['id']

        try:
            tt = TwitterTracks.objects.get(id=id)
            current_user = request.user
            tt.user.remove(current_user)
        except Exception as e:
            error_report(e)

    return HttpResponse(1)
