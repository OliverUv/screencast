from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from account import views

urlpatterns = patterns('',
    url(r'^index/$', views.index, name='index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^browse/$', views.browse, name='browse'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^test/$', views.test, name='test'),
    url(r'^profile/share/$', views.share, name='share'),
    url(r'^share_add_users/$', views.share_add_users, name='share_add_users'),
    url(r'^test/create_group/$', views.create_group, name='create_group'),
    url(r'^test/get_group/$', views.get_group, name='get_group'),
    url(r'^launch_applet/$', views.launch_applet, name='launch_applet'),
   )
