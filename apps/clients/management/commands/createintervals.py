from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule


class Command(BaseCommand):
    help = 'Creates intervals for service: 1, 7, 30 days'

    def handle(self, *args, **options):
        IntervalSchedule.objects.create(every=1, period=IntervalSchedule.DAYS)
        IntervalSchedule.objects.create(every=7, period=IntervalSchedule.DAYS)
        IntervalSchedule.objects.create(every=30, period=IntervalSchedule.DAYS)
        print('Intervals have been created successfully!')
