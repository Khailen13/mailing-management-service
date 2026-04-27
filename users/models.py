from django.contrib.auth.models import AbstractUser
from django.db import models


# В модель пользователя добавлены поля email, аватар, номер телефона, страна в соответствующих типах.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Адрес эл. почты")
    phone_number = models.CharField(max_length=35, verbose_name="Номер телефона", blank=True, null=True)
    avatar = models.ImageField(upload_to="users/avatars/", verbose_name="Аватар", blank=True, null=True)
    country = models.CharField(max_length=70, verbose_name="Страна", blank=True, null=True)

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]
        permissions = [
            ("change_user_activity", "Can change user activity"),
            ("view_users_list", "Can view users list"),
        ]

    def __str__(self):
        return self.email
