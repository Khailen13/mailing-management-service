from django.contrib import admin

from mailing.models import Mailing, MailingAttempt, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "email",
        "full_name",
        "comment",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "subject",
        "body",
    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "start_datetime",
        "end_datetime",
        "status",
        "message",
        "is_active",
    )


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "mailing",
        "recipient",
        "status",
        "attempt_datetime",
        "server_response",
    )
