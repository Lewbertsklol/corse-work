from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates ALL initial data'

    def handle(self, *args, **options):
        call_command('migrate')
        call_command('creategroup', 'manager')
        call_command('createintervals')
        call_command('createposts')
