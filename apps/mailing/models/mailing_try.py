from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.main.models import AbstractModel


class MailingTry(AbstractModel):
    mailing = models.ForeignKey('mailing.Mailing', on_delete=models.CASCADE, verbose_name=_('Рассылка'))
    status = models.BooleanField(verbose_name=_('Статус'))
    email_server_answer = models.TextField(verbose_name=_('Ответ сервера'))
    runned_at = models.DateTimeField(verbose_name=_('Время запуска'))

    def __str__(self):
        return self.runned_at

    class Meta:
        verbose_name = _("Попытка рассылки")
        verbose_name_plural = _("Попытки рассылки")
