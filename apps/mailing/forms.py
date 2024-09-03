from datetime import datetime

from django import forms

from django_celery_beat.models import IntervalSchedule

from apps.clients.models import Client
from apps.mailing.models import Message


class MailingForm(forms.Form):
    name = forms.CharField(required=True)
    interval = forms.ModelChoiceField(queryset=IntervalSchedule.objects.all(), required=True)
    enabled = forms.BooleanField(initial=False, required=False)
    datetime = forms.DateTimeField(initial=datetime.now(), required=True)
    message = forms.ModelChoiceField(Message.objects.none(), required=True)
    clients = forms.ModelMultipleChoiceField(Client.objects.none(), required=True)

    def __init__(self, user, *args, **kwargs):
        # Требуется переопределние полей под конкретных юзеров
        super().__init__(*args, **kwargs)
        self.fields['message'].queryset = Message.objects.filter(user=user)
        self.fields['clients'].queryset = Client.objects.filter(user=user)
