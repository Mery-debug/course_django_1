from django.db import models


class SendingUser:
    email = models.EmailField(unique=True)
    fio = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"{self.email} - {self.fio}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["email"]


class Email:
    subject= models.CharField(max_length=100, verbose_name="subject mail")
    text = models.TextField(max_length=1500, verbose_name="text")

    def __str__(self):
        return f"{self.subject} {self.text}"

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        ordering = ["subject_mail"]


class Sending:
    date_fist = models.DateField()
    date_last = models.DateField()
    status = models.CharField()
    mail = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='Письмо', blank=True, null=True)
    users = models.ManyToManyField(SendingUser, on_delete=models.CASCADE, related_name='Получатели рассылки', blank=True, null=True)

    def __str__(self):
        return f"{self.mail} {self.users} {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["mail"]


class SendTry:
    pass

