from django.contrib.auth.models import AbstractUser
from django.db import models


class Auth(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Адрес почты")
    img = models.ImageField(
        upload_to="media/img/", blank=True, null=True, verbose_name="Изображение"
    )
    country = models.CharField(null=True, blank=True, verbose_name="Страна")
    phone_number = models.IntegerField(
        null=True, blank=True, help_text="Номер должен содержать только цифры"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['email']


