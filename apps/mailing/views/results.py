from django.views import generic
from django.urls import reverse, reverse_lazy
from django_celery_results.models import TaskResult

from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin

from apps.mailing.models import Mailing


class ResultListView(LoginRequiredMixin, generic.ListView):
    model = TaskResult
    template_name = 'mailing/results/results_list.html'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        task_name = Mailing.objects.get(
            id=self.kwargs['pk']
        ).sending_task.name

        return TaskResult.objects.filter(periodic_task_name=task_name)


class ResultDeleteView(LoginRequiredMixin, AccessMixin, generic.DeleteView):
    model = TaskResult
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        result_task = self.get_object().periodic_task_name
        pk = Mailing.objects.get(sending_task__name=result_task).id
        return reverse('mailing:results_list', kwargs={'pk': pk})

    def dispatch(self, request, *args, **kwargs):
        result_task = self.get_object().periodic_task_name
        if Mailing.objects.get(sending_task__name=result_task).user != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
