from django.db import models
from django.contrib.auth.models import User, Group


class UserProfile(models.Model):
    user = models.OneToOneField(User)


def get_or_create_profile(user):
    profile, c = UserProfile.objects.get_or_create(user=user)
    if not c:
        return profile
    profile = UserProfile(user=user)
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
    filename = models.CharField(max_length=200)
    disp_name = models.CharField(max_length=200)
    upload_date = models.CharField(max_length=10)

    def __unicode__(self):
        return self.filename

    class Meta:
        permissions = (
            ('modify_resource', 'Able to modify resource'),
            ('view_resource', 'Able to view resource'),
        )


def create_group(group_name, creator):
    '''
    Creates and returns a group, ensuring that the creator has
    the proper rights pertaining to the group.
    '''
    g = Group(creator=creator, name=group_name)
    g.save()
    g.observers.add(creator)
    return g
