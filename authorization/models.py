from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Auth(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Адрес почты")
    img = models.ImageField(
        upload_to="media/img/", blank=True, null=True, verbose_name="Изображение"
    )
    country = models.CharField(null=True, blank=True, verbose_name="Страна")
    phone_number = models.IntegerField(
        null=True, blank=True, help_text="Номер должен содержать только цифры"
    )
    code = models.IntegerField(max_length=4, null=True, blank=True)
    is_auth = models.BooleanField(default=True, null=True, blank=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        self.is_active = True
        return reverse("authorization:access_code")

    # @property
    # def is_manag(self) -> bool:
    #     return self.groups.filter(name=MANAG_GROUP).exists()




    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['email']


