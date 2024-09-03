import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from django_celery_beat.models import PeriodicTask

from apps.mailing.models import Mailing
from apps.mailing.forms import MailingForm
from apps.main.permissions import OwnerPermissionMixin


class MailingListView(LoginRequiredMixin, generic.ListView):
    model = Mailing
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        return Mailing.objects.filter(user=self.request.user)


class MailingCreateView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('users:login')

    def get(self, request):
        return render(request, 'mailing/mailing_form.html', {'form': MailingForm(request.user)})

    def post(self, request):
        form = MailingForm(request.user, request.POST)
        if form.is_valid():
            task = PeriodicTask.objects.create(
                # добавляем email пользователя к имени таски, чтобы не было конфликтов по имени у разных пользователей
                name=request.user.email + '::' + form.cleaned_data['name'],
                interval=form.cleaned_data['interval'],
                task='send_email',
                start_time=form.cleaned_data['datetime'],
                enabled=form.cleaned_data['enabled'],
                kwargs=json.dumps({
                    'message_id': form.cleaned_data['message'].id,
                    'clients_id': list(form.cleaned_data['clients'].values_list('id', flat=True))
                }),
            )
            mailing = Mailing.objects.create(
                sending_task=task,
                message=form.cleaned_data['message'],
                user=request.user
            )
            mailing.clients.set(form.cleaned_data['clients'])
            return redirect('mailing:mailing_list')
        return render(request, 'mailing/mailing_form.html', {'form': form})


class MailingUpdateView(LoginRequiredMixin, OwnerPermissionMixin, generic.View):
    login_url = reverse_lazy('users:login')

    def get_object(self):
        return Mailing.objects.get(id=self.kwargs['pk'])

    def get(self, request, pk):
        mailing = self.get_object()
        form = MailingForm(request.user, data={
            'name': mailing.name,
            'interval': mailing.interval,
            'datetime': mailing.start_time,
            'enabled': mailing.is_active,
            'message': mailing.message,
            'clients': mailing.clients.all()
        })
        return render(request, 'mailing/mailing_form.html', {'form': form})

    def post(self, request, pk):
        form = MailingForm(request.user, request.POST)
        if form.is_valid():
            mailing = Mailing.objects.get(id=pk)
            mailing.delete()
            task = PeriodicTask.objects.create(
                name=request.user.email + '::' + form.cleaned_data['name'],
                interval=form.cleaned_data['interval'],
                task='mailing.tasks.send_email',
                start_time=form.cleaned_data['datetime'],
                enabled=form.cleaned_data['enabled'],
                kwargs=json.dumps({
                    'message_id': form.cleaned_data['message'].id,
                    'clients_id': list(form.cleaned_data['clients'].values_list('id', flat=True))
                }),
            )
            mailing = Mailing.objects.create(
                sending_task=task,
                message=form.cleaned_data['message'],
                user=request.user
            )
            mailing.clients.set(form.cleaned_data['clients'])
            return redirect('mailing:mailing_list')

        return render(request, 'mailing/mailing_form.html', {'form': form})


class MailingDeleteView(LoginRequiredMixin, OwnerPermissionMixin, generic.DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = reverse_lazy('users:login')


@login_required(login_url=reverse_lazy('users:login'))
def toggle_mailing(request: HttpRequest, pk):
    mailing = Mailing.objects.get(id=pk)
    mailing.sending_task.enabled = not mailing.sending_task.enabled
    mailing.sending_task.save()
    return redirect(request.META.get('HTTP_REFERER'))


class ManagerMailingListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Mailing
    permission_required = 'mailing.view_mailing'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        return Mailing.objects.filter(user__id=self.kwargs['pk'])
