from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.main.models import AbstractModel


class Message(AbstractModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("Пользователь"),
    )
    title = models.CharField(_("Заголовок"), max_length=255)
    body = models.TextField(_("Сообщение"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Сообщение")
        verbose_name_plural = _("Сообщения")
