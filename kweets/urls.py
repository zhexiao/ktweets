from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tweets/', include('tweets.urls', namespace='tweets', app_name='tweets'))
]
