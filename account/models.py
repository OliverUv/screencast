import os
import datetime

from django.db import models
from django.contrib.auth.models import User, Group
from hashlib import sha224


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    upload_token = models.CharField(max_length=100)


def get_or_create_profile(user):
    profile, c = UserProfile.objects.get_or_create(user=user)
    if not c:
        return profile
    # profile = UserProfile(user=user)
    try:
        rand_seed = os.urandom(40)
    except NotImplementedError:
        # This string is not cryptographically safe
        rand_seed = user.username + str(datetime.datetime.now().time())
        rand_seed += ''.join(os.uname()) + str(os.getpid())
        print
        '''Warning: using unsafe upload tokens for uploads.
        Recommend running on an os with true random support.'''

    profile.upload_token = sha224(rand_seed).hexdigest()
    profile.save()
    return profile

User.profile = property(get_or_create_profile)

# Make it possible to associate groups with users, so that each user
# can create and view their own groups independently of one another.
if not hasattr(Group, 'creator'):
    field = models.ForeignKey(User, blank=False, null=False, related_name='created_groups')
    field.contribute_to_class(Group, 'creator')

# Make it possible to share groups between users.
if not hasattr(Group, 'observers'):
    field = models.ManyToManyField(User, related_name='known_groups')
    field.contribute_to_class(Group, 'observers')


class Resource(models.Model):
    # Screencast files, audio tracks, etc.
    key = models.ForeignKey(User)
    cast_uuid = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    disp_name = models.CharField(max_length=200)
    upload_date = models.CharField(max_length=10)
    creation_timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.filename

    class Meta:
        permissions = (
            ('modify_resource', 'Able to modify resource'),
            ('view_resource', 'Able to view resource'),
        )


def create_group(group_name, creating_user):
    '''
    Creates and returns a group, ensuring that the creator has
    the proper rights pertaining to the group.
    '''
    g = Group(creator=creating_user, name=group_name)
    g.save()
    g.observers.add(creating_user)
    return g
