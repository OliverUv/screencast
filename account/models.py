from django.db import models
from django_cas.backends import CASBackend
from django.contrib.auth.models import User 

class UserProfile(models.Model):
    user = models.OneToOneField(User)

class Resource(models.Model):
    #Screencast files, audio tracks, etc. 
    key = models.ForeignKey(User);
    filename = models.CharField(max_length=200)
    
    def __unicode__(self):
        return filename
