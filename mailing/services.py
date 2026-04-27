from django.core.cache import cache

from config.settings import CACHE_ENABLED
from mailing.models import Mailing, MailingAttempt, Message, Recipient


def get_data_from_cache(model, user):
    """Получает данные пользователя (клиенты, сообщения, рассылки, попытки рассылки) из кэша или из базы данных."""

    if not CACHE_ENABLED:
        if model in [Recipient, Message, Mailing]:
            return [
                object
                for object in model.objects.all()
                if object.owner == user or user.is_superuser or user.groups.filter(name="managers").exists()
            ]
        elif model == MailingAttempt:
            return [
                object
                for object in MailingAttempt.objects.all()
                if object.mailing.owner == user or user.is_superuser or user.groups.filter(name="managers").exists()
            ]
    key = f"{model}-{user.id}"
    data = cache.get(key)
    if data:
        return data
    if model in [Recipient, Message, Mailing]:
        data = [
            object
            for object in model.objects.all()
            if object.owner == user or user.is_superuser or user.groups.filter(name="managers").exists()
        ]
    elif model == MailingAttempt:
        data = [
            object
            for object in MailingAttempt.objects.all()
            if object.mailing.owner == user or user.is_superuser or user.groups.filter(name="managers").exists()
        ]

    cache.set(key, data)
    return data
