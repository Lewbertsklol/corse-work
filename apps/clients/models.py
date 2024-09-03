from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.main.models import AbstractModel


class Client(AbstractModel):
    name = models.CharField(max_length=255, verbose_name=_("ФИО"))
    email = models.EmailField(verbose_name=_("Email"))
    comment = models.TextField(verbose_name=_("Комментарий"), blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clients",
        verbose_name=_('Пользователь'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Клиент")
        verbose_name_plural = _("Клиенты")
