from django.core.management.base import BaseCommand, CommandError
from account.models import Resource
from django.contrib.auth.models import User, Group, Permission

class Command(BaseCommand):
    args = '<init_type init_type ...>'
    help = 'Initializes database with data. Init_types: init_groups, init_test'

    def handle(self, *args, **options):
        for init_type in args:
            #-- Create groups --
            if init_type == 'init_groups':
                #Students
                gStudents, c = Group.objects.get_or_create(name='students')
                if c:
                    gStudents.permissions.add(Permission.objects.get(codename='view_resource'))

                #Admins
                gAdmins, c = Group.objects.get_or_create(name='admins')
                if c:
                    gAdmins.permissions.add(Permission.objects.get(codename='view_resource'),
                                            Permission.objects.get(codename='modify_resource'),
                                            )

            #-- Create test data --
            if init_type == 'init_test':
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
