from django.contrib import admin

from account.models import Resource, UserProfile

# Note that the django admin will display all times as if you are in
# central America.

admin.site.register(Resource)
admin.site.register(UserProfile)
