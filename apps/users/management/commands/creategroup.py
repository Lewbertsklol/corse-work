from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from apps.mailing.models import Mailing


def get_permissions(model, codenames):
    content_type = ContentType.objects.get_for_model(model)
    return [*Permission.objects.filter(
        content_type=content_type,
        codename__in=codenames
    )]


class Command(BaseCommand):
    help = 'Creates group for users'

    def add_arguments(self, parser):
        parser.add_argument('group', type=str)

    def handle(self, *args, **options):

        match options['group']:
            case 'manager':
                group = Group.objects.create(name='manager')
                permissions = (
                    get_permissions(Mailing, ['view_mailing']) +
                    get_permissions(get_user_model(), ['can_ban_users', 'can_unban_users', 'view_user'])
                )
                group.permissions.set(permissions)
            case _:
                raise ValueError('Unknown group')

        print(f'Group {options['group']} have been created successfully!')
