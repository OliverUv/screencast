from django.db import models
from django_cas.backends import CASBackend
from django.contrib.auth.models import User 
from django.utils import simplejson

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #Assign groups 

def get_or_create_profile(user):
    profile, c = UserProfile.objects.get_or_create(user=user)
    if not c:
        return profile;
    profile = UserProfile(user=user)
    profile.save()
    return profile;

User.profile = property(get_or_create_profile)

class Resource(models.Model):
    #Screencast files, audio tracks, etc. 
    key = models.ForeignKey(User);
    filename = models.CharField(max_length=200)

    def __unicode__(self):
        return self.filename

    class Meta:
        permissions=(
            ('modify_resource', 'Able to modify resource'),
            ('view_resource', 'Able to view resource'),
        )

# JSON encoder
class LazyEncoder(simplejson.JSONEncoder):
    """Encodes django's lazy i18n strings.
    """
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj
