from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('account.urls', namespace='account')),
    (r'^accounts/login/$', 'django_cas.views.login'),
    (r'^accounts/logout/$', 'django_cas.views.logout'),
)
