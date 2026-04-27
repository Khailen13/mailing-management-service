from django.db import models
from django.db.models import ForeignKey
from django.template.defaultfilters import truncatechars

from users.models import User


class Recipient(models.Model):
    email = models.CharField(unique=True, max_length=254, verbose_name="Адрес электронной почты")
    full_name = models.CharField(max_length=150, verbose_name="Ф.И.О.", blank=True, null=True)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", blank=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["-id"]


class Message(models.Model):
    subject = models.CharField(max_length=120, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", blank=True, null=True)

    def __str__(self):
        return truncatechars(self.subject, 85)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-id"]


class Mailing(models.Model):
    start_datetime = models.DateTimeField(verbose_name="Дата и время первой отправки", blank=True, null=True)
    end_datetime = models.DateTimeField(verbose_name="Дата и время окончания отправки", blank=True, null=True)
    STATUS_CHOICES = {
        "created": "Создана",
        "launched": "Запущена",
        "completed": "Завершена",
    }
    status = models.CharField(choices=STATUS_CHOICES, default="created", verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    recipients = models.ManyToManyField(
        Recipient,
        related_name="recipients",
        verbose_name="Получатели рассылки",
        help_text="Для выделения нескольких получателей используйте комбинации ЛКМ+Ctrl или ЛКМ+Shift.",
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Допуск рассылки")

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-id"]
        permissions = [
            ("change_mailing_activity", "Can change mailing activity"),
        ]


class MailingAttempt(models.Model):
    attempt_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    STATUS_CHOICES = {
        "successfully": "успешно",
        "unsuccessfully": "не успешно",
    }
    status = models.CharField(choices=STATUS_CHOICES, blank=True, null=True, verbose_name="Статус")
    server_response = models.TextField(blank=True, null=True, verbose_name="Ответ почтового сервера")
    mailing = ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")
    recipient = ForeignKey(Recipient, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Получатель")

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["-id"]

    def __str__(self):
        return str(self.pk)
