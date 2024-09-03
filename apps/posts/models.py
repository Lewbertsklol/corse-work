from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.main.models import AbstractModel


class Post(AbstractModel):
    title = models.CharField(_("Заголовок"), max_length=255)
    text = models.TextField(_("Текст"))
    image = models.ImageField(_("Изображение"), upload_to="posts", blank=True, null=True)
    views_count = models.PositiveIntegerField(_("Количество просмотров"), default=0)

    class Meta:
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
