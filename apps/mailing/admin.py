from django.contrib import admin

from .models import Mailing, Message

admin.site.register((Message))


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'message', 'start_time', 'interval')
