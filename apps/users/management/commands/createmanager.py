from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates manager account'

    def handle(self, *args, **options):
        user = get_user_model().objects.create(
            email=input('Enter email: '),
            password=input('Enter password: ')
        )
        user.groups.set([Group.objects.get(name='manager')])
        print('Manager account have been created successfully!')
