from django.conf.urls import url
from tweets.views import *

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'stream$', views.stream, name='stream'),
    url(r'twitter_mention/lists\/?$', twitter_mention_view.TwitterMentionLists.as_view()),
]
