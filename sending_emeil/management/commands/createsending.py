from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from config import settings
from sending_emeil.models import SendTry, Sending


class Command(BaseCommand):
    help = "Отправка рассылки по требованию"

    def add_arguments(self, parser):
        parser.add_argument("pk", type=int, help="ID рассылки для отправки")

    def handle(self, *args, **kwargs):
        pk = kwargs["pk"]
        try:
            sending = Sending.objects.get(id=pk)
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f"Рассылка с ID {pk} не найдена."))
            return
        if sending.status != Sending.CREATED:
            self.stdout.write(
                self.style.WARNING(
                    f"Рассылка с ID {pk} не может быть отправлена, так как ее статус: {sending.status}."
                )
            )
            return
        sending.status = Sending.STARTED
        sending.first_sending = timezone.now()
        sending.save()
        for contact in sending.contact.all():
            attempt = SendTry(sending=sending)
            try:
                send_mail(
                    sending.message.subject,
                    sending.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[contact.email],
                    fail_silently=False,
                )
                attempt.status = SendTry.SUCCESS
                attempt.server_response = "Письмо отправлено успешно."
                self.stdout.write(self.style.SUCCESS(f"Письмо отправлено на {contact.email}."))
            except Exception as e:
                attempt.status = SendTry.FAILURE
                attempt.server_response = str(e)
                self.stdout.write(self.style.ERROR(f"Ошибка при отправке на {contact.email}: {e}"))

            attempt.save()

        sending.status = Sending.COMPLETED
        sending.end_sending = timezone.now()
        sending.save()
        self.stdout.write(self.style.SUCCESS("Рассылка успешно отправлена!"))
