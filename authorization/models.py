from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from config.settings import MANAG_GROUP


class Auth(AbstractUser):
    username = models.CharField(verbose_name="Имя пользователя")
    email_address = models.EmailField(unique=True)
    img = models.ImageField(
        upload_to="media/img/", blank=True, null=True, verbose_name="Изображение"
    )
    country = models.CharField(null=True, blank=True, verbose_name="Страна")
    phone_number = models.CharField(
        null=True, blank=True, help_text="Номер должен содержать только цифры"
    )
    code = models.IntegerField(null=True, blank=True)
    is_auth = models.BooleanField(default=False, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    USERNAME_FIELD = "email_address"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email_address

    def get_absolute_url(self):
        self.is_active = True
        return reverse("authorization:access_code")

    @property
    def is_manag(self) -> bool:
        return self.groups.filter(name=MANAG_GROUP).exists()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['email_address']


class Code(models.Model):
    code = models.CharField(unique=True, help_text="Код из сообщения")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'код подтверждения'
        verbose_name_plural = 'коды подтверждения'
        ordering = ['code']
