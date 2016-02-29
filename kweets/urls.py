from django.conf.urls import url, include
from django.contrib import admin
from tweets import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^tweets/', include('tweets.urls', namespace='tweets', app_name='tweets')),
    url(r'^account/', include('account.urls', namespace='account', app_name='account')),
]
