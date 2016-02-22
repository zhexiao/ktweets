from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # url(r'^login/$', views.user_login, name='login'),
    # url(r'^register/$', views.user_register, name='register'),

    url(r'^login/$', auth_views.login, {
        'template_name':'account/login.html'
    }, name='login'),
    url(r'^register/$', views.user_register, name='register'),
    url(r'^logout/$', auth_views.logout, {
        'template_name':'account/logout.html'
    }, name='logout'),
    url(r'^logout-then-login/$', auth_views.logout_then_login, name='logout_then_login'),
    url(r'^password-change/$', auth_views.password_change,  {
        'template_name':'account/password_change.html',
        'post_change_redirect':'account:password_change_done'
    }, name='password_change'),
    url(r'^password-change-done/$', auth_views.password_change_done, {
        'template_name':'account/password_change_done.html',
    }, name='password_change_done'),
]
