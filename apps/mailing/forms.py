from datetime import datetime

from django import forms
from django_celery_beat.models import IntervalSchedule

from apps.clients.models import Client
from apps.mailing.models import Message


class MailingForm(forms.Form):
    name = forms.CharField(required=True)
    interval = forms.ModelChoiceField(queryset=IntervalSchedule.objects.all(), required=True)
    enabled = forms.BooleanField(initial=False)
    date = forms.DateField(initial=datetime.now().date(), widget=forms.SelectDateWidget(), required=True)
    time = forms.TimeField(initial=datetime.now().time(), required=True)

    # Требуется переопределние полей под конкретных юзеров
    message = forms.ModelChoiceField(Message.objects.all(), required=True)
    clients = forms.ModelMultipleChoiceField(Client.objects.all(), required=True)
