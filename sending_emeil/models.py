from django.db import models


class SendingUser(models.Model):
    email = models.EmailField(unique=True)
    fio = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"{self.email} - {self.fio}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["email"]


class Email(models.Model):
    subject = models.CharField(max_length=100, verbose_name="Тема письма")
    text = models.TextField(max_length=1500, verbose_name="Текст письма")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        ordering = ["subject"]


class Sending(models.Model):
    date_first = models.DateField(verbose_name="Дата начала")
    date_last = models.DateField(verbose_name="Дата окончания")
    status = models.CharField(max_length=50, verbose_name="Статус")
    mail = models.ForeignKey(
        Email,
        on_delete=models.CASCADE,
        related_name='Письма',
        blank=True,
        null=True,
        verbose_name="Письма"
    )
    users = models.ManyToManyField(
        SendingUser,
        related_name='Получатели',
        blank=True,
        verbose_name="Получатели"
    )

    def __str__(self):
        return f"Рассылка #{self.id} ({self.status})"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["mail"]


class SendTry:
    pass

