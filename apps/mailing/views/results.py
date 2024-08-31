from django.views import generic
from django_celery_results.models import TaskResult
from django_celery_beat.models import PeriodicTask

from apps.mailing.models import Mailing


class ResultListView(generic.ListView):
    model = TaskResult

    def get_queryset(self):
        tasks = Mailing.objects.filter(user=self.request.user)
