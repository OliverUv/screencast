from django.conf.urls import patterns, url
from account import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^my_files/$', views.my_files, name='my_files'),
    url(r'^my_files/change_name/$', views.change_name, name='change_name'),
    url(r'^my_files/remove_resource/$', views.remove_resource, name='remove_resource'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^groups/$', views.groups, name='groups'),
    url(r'^complete_users_and_groups/(?P<completion_string>\w+)/$', views.complete_users_and_groups, name='complete_usernames'),
    url(r'^profile/share/$', views.share, name='share'),
    url(r'^share_add_users/$', views.share_add_users, name='share_add_users'),
    url(r'^groups/create_group/$', views.create_group, name='create_group'),
    url(r'^groups/get_group/$', views.get_group, name='get_group'),
    url(r'^launch_applet/$', views.launch_applet, name='launch_applet'),
)
