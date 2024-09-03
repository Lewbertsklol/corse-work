import smtplib

from celery import shared_task
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from apps.mailing.models import Message
from apps.clients.models import Client


@shared_task(name='send_email')
def send_email(*, message_id: int, clients_id: list):
    message = Message.objects.get(id=message_id)
    try:
        send_mail(
            subject=message.title,
            message=message.body,
            from_email=None,
            recipient_list=Client.objects.filter(id__in=clients_id).values_list('email', flat=True),
            fail_silently=False
        )
        return 'All messages are sent'
    except smtplib.SMTPException as e:
        return f'Error: {e}'
