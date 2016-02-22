from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # url(r'^login/$', views.user_login, name='login'),
    # url(r'^register/$', views.user_register, name='register'),

    url(r'^login/$', auth_views.login, {'template_name':'account/login.html'}, name='login'),
    url(r'^register/$', views.user_register, name='register'),
    url(r'^logout/$', auth_views.logout, {'template_name':'account/logout.html'}, name='logout'),
    url(r'^logout-then-login/$', auth_views.logout_then_login, name='logout_then_login')
]
