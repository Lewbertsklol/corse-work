from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.main.models import AbstractModel


class Mailing(AbstractModel):
    message = models.ForeignKey(
        'mailing.Message',
        on_delete=models.CASCADE,
        verbose_name=_('Сообщение'),
    )
    sending_task = models.ForeignKey(
        'django_celery_beat.PeriodicTask',
        on_delete=models.CASCADE,
        verbose_name=_('Задача'),
    )

    clients = models.ManyToManyField(
        'clients.Client',
        verbose_name=_('Клиенты'),
        blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name=_('Пользователь'),
    )

    @property
    def name(self):
        return self.sending_task.name

    name.fget.short_description = _("Название")

    @property
    def is_active(self):
        return self.sending_task.enabled

    is_active.fget.short_description = _("Активна")

    @property
    def interval(self):
        return self.sending_task.interval

    interval.fget.short_description = _("Интервал")

    @property
    def start_time(self):
        return self.sending_task.start_time

    start_time.fget.short_description = _("Первый запуск")
    
    


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Рассылка")
        verbose_name_plural = _("Рассылки")


@receiver(post_delete, sender=Mailing)
def delete_periodic_task(sender, instance, **kwargs):
    instance.sending_task.delete()
