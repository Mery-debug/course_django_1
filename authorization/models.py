from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import MANAG_GROUP


class Auth(AbstractUser):
    email_address = models.EmailField(unique=True, verbose_name="адрес почты")
    is_active = models.BooleanField(default=True, null=True, blank=True)
    password_reset_token = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        unique=True
    )

    USERNAME_FIELD = "email_address"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email_address}"


    @property
    def is_manag(self) -> bool:
        return self.groups.filter(name=MANAG_GROUP).exists()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['email_address']


class Code(models.Model):
    code = models.CharField(unique=True, help_text="Код из сообщения")
    user = models.ForeignKey(Auth, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'код подтверждения'
        verbose_name_plural = 'коды подтверждения'
        ordering = ['code']
