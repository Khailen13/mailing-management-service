from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Создает группу менеджеров с требуемыми правами"""

    def handle(self, *args, **options):

        managers_group = Group.objects.create(name="Managers2")
        permissions = dict()
        permissions["change_mailing_activity_permission"] = Permission.objects.get(codename="change_mailing_activity")
        permissions["view_mailing_permission"] = Permission.objects.get(codename="view_mailing")
        permissions["view_mailingattempt_permission"] = Permission.objects.get(codename="view_mailingattempt")
        permissions["view_message_permission"] = Permission.objects.get(codename="view_message")
        permissions["view_recipient_permission"] = Permission.objects.get(codename="view_recipient")
        permissions["change_user_activity_permission"] = Permission.objects.get(codename="change_user_activity")
        permissions["view_user_permission"] = Permission.objects.get(codename="view_user")
        permissions["view_users_list_permission"] = Permission.objects.get(codename="view_users_list")

        for permission in permissions:
            managers_group.permissions.add(permissions[permission])
