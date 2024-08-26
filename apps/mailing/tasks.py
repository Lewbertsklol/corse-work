from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.mailing.models import Message
from apps.clients.models import Client


@shared_task(name='send_email')
def send_email(*, user_id, message_id, clients_id):
    message = Message.objects.get(id=message_id)
    user = get_user_model().objects.get(id=user_id)
    return send_mail(
        subject=message.title,
        message=message.body,
        from_email=None,  # user.email
        recipient_list=Client.objects.filter(id__in=clients_id).values_list('email', flat=True),
    )
