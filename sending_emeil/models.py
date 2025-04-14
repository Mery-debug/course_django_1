from django.db import models


class SendingUser(models.Model):
    email = models.EmailField(unique=True)
    fio = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"{self.email} - {self.fio}"

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
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
    CREATED = "created"
    STARTED = "started"
    COMPLETED = "completed"

    MAILING_STATUSES = [
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
        (COMPLETED, "Завершена"),
    ]

    date_first = models.DateField(blank=True, null=True, verbose_name="Дата начала")
    date_last = models.DateField(blank=True, null=True, verbose_name="Дата окончания")
    status = models.CharField(max_length=10, choices=MAILING_STATUSES, default=CREATED, verbose_name="Статус")
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
    SUCCESS = "success"
    FAILURE = "fail"
    CREAT = "on_stop"
    STOP = "canceled"

    send_try_status = [
        (SUCCESS, "успешная рассылка"),
        (FAILURE, "рассылка провалилась"),
        (CREAT, "приостановлена (не запущена)"),
        (STOP, "прекращена")
    ]

    status = models.CharField(choices=send_try_status, default=CREAT, blank=True, null=True)
    date_of_try = models.DateField(auto_now=True)
    answer_server = models.TextField(blank=True, null=True)
    sending = models.ForeignKey(Sending, on_delete=models.CASCADE)

    def __str__(self):
        return f"Попытка рассылки {self.status} {self.date_of_try}"


