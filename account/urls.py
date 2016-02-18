from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^login/$', views.user_login, name='login'),
    # url(r'^register/$', views.user_register, name='register'),
    
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':'account/login.html'}, name='login'),
    url(r'^register/$', views.user_register, name='register'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name':'account/logout.html'}, name='logout'),
    url(r'^logout-then-login/$', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),
]