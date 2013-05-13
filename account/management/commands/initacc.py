from django.core.management.base import BaseCommand, CommandError
from account.models import Resource
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Initializes some test data'

    def handle(self, *args, **options):
        #Create test user
        user, c = User.objects.get_or_create(
            username='testpilot', password='tester')

        #Create resources
        r, c = Resource.objects.get_or_create(
            key=user,
            filename='resource1')
        r, c = Resource.objects.get_or_create(
            key=user,
            filename='resource2')

        self.stdout.write('Successfully created test data' )
