from django.contrib import admin

from account.models import Resource, UserProfile


admin.site.register(Resource)
admin.site.register(UserProfile)
