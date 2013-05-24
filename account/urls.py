from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from account import views

urlpatterns = patterns('',
    url(r'^index/$', views.index, name='index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^browse/$', views.browse, name='browse'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^test/$', views.test, name='test'),
    url(r'^share/$', views.share, name='share'),
    url(r'^share_add_users/$', views.share_add_users, name='share_add_users'),
#    url(r'^(?P<user_id>\d+)/$', views.detail, name='detail'),
   )
