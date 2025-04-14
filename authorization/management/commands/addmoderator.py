from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

import sending_emeil


class Command(BaseCommand):
    help = 'Создание группы модератор продуктов'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Manager')

        can_unpublish_product = Permission.objects.get(
            codename='can_unpublish_sending',
            content_type__app_label='sending_emeil',
            content_type__model='sending'
        )

        delete_product = Permission.objects.get(
            codename='delete_sending',
            content_type__app_label='sending_emeil',
            content_type__model='sending'
        )

        group.permissions.add(can_unpublish_sending, delete_sending)