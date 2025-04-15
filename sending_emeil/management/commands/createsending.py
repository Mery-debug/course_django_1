from django.core.management.base import BaseCommand


class CreateSending(BaseCommand):
    help = "Команда создает рассылку на заранее прописанные адреса"

    def handle(self, *args, **kwargs):
        sending_list = [
            "sample@example.ru",
            "example@sample.ru",
            "sample@sample.com",
            "amin@amin.com",
            "get@mail.com"
        ]

