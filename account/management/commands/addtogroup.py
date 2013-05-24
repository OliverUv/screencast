from django.core.management.base import BaseCommand, CommandError
from account.models import Resource
from django.contrib.auth.models import User, Group, Permission

class Command(BaseCommand):
    args = '<group user rm/add>'
    help = 'Adds user to specified group. Last argument specifies remove (rm) or add (add) to group' 

    def handle(self, *args, **options):
        if not len(args) == 3:
            self.stdout.write('Invalid argument. Arguments: <command> user group')
            return

        try:
            group = Group.objects.get(name=args[1])
        except Group.DoesNotExist:
            self.stdout.write('Group not found')
            return
        try:
            user = User.objects.get(username=args[0])
        except User.DoesNotExist:
            self.stdout.write('User not found')
            return
        
        if args[2] == 'rm':
            user.groups.remove(group)
        if args[2] == 'add':
            user.groups.add(group)
