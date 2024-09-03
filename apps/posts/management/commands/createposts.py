from django.core.management.base import BaseCommand

from apps.posts.models import Post


class Command(BaseCommand):
    help = 'Creates posts'

    def handle(self, *args, **options):
        Post.objects.create(
            title='OwnerPermissionMixin',
            text='Миксин для проверки принадлежности запрашиваемого объекта пользователю. Добавляется в CBV. '
        )
        Post.objects.create(
            title='Django_celery_beat',
            text='Библиотека для работы с периодическими задачами. Настраивается задача и интервал её исполнения. '
            'Модель django_celery_beat.PeriodicTask привязана к mailing.Mailing. '
            'Удаление и Mailing и PeriodicTask одновременно работает через сигналы. '
        )
        Post.objects.create(
            title='Django_celery_results',
            text='Библиотека для хранения результатов выполнения задач. '
            'Уже содержит в себе дату выполнения задачи, статус и результат выполнения. '
        )
        Post.objects.create(
            title='Manager Group',
            text='Хотя в интерфейсе менеджера и есть кнопка "создать рассылку", '
            'при просмотре рассылок пользователей, рассылка создается непосредственно для самого менеджера. '
        )

        print('Posts have been created successfully!')
