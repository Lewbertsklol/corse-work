import json
from datetime import datetime

from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django_celery_beat.models import PeriodicTask

from apps.clients.models import Client
from apps.mailing.models import Mailing, Message
from apps.mailing.forms import MailingForm
# Create your views here.


class MailingListView(generic.ListView):
    model = Mailing

    def get_queryset(self):
        return Mailing.objects.filter(user=self.request.user)


class MailingDetailView(generic.DetailView):
    model = Mailing


class MailingCreateView(generic.View):

    def get(self, request):
        return render(request, 'mailing/mailing_form.html', {'form': MailingForm(request.user)})

    def post(self, request):
        form = MailingForm(request.user, request.POST)
        if form.is_valid():
            task = PeriodicTask.objects.create(
                name=request.user.email + '::' + form.cleaned_data['name'],
                interval=form.cleaned_data['interval'],
                task='send_email',
                start_time=datetime.combine(form.cleaned_data['date'], form.cleaned_data['time']),
                enabled=form.cleaned_data['enabled'],
                kwargs=json.dumps({
                    'user_id': request.user.id,
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


class MailingUpdateView(generic.View):

    def get(self, request, pk):
        mailing = Mailing.objects.get(id=pk)
        form = MailingForm(request.user, data={
            'name': mailing.name,
            'interval': mailing.interval,
            'date': mailing.start_time.date(),
            'time': mailing.start_time.time(),
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
                start_time=datetime.combine(form.cleaned_data['date'], form.cleaned_data['time']),
                enabled=form.cleaned_data['enabled'],
                kwargs=json.dumps({
                    'user_id': request.user.id,
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


class MailingDeleteView(generic.DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
