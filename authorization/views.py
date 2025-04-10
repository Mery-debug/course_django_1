from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from authorization.forms import CodeForm, AuthForm
from authorization.models import Auth
from authorization.services import random_code_generator
from config.settings import EMAIL_HOST_USER
from sending_emeil.models import SendingUser

code = next(random_code_generator())


class AccessCodeView(TemplateView):
    model = Auth
    form = CodeForm
    template_name = "authorization/access_code.html"

    def get_success_url(self):
        code_user = self.request.code
        if code_user == code:
            Auth.is_active = True
            return reverse_lazy("sending_emeil:home")
        Auth.is_active = False
        raise ValidationError("Вы ввели не верный код")


    def send_verification_email(self, request):
        if self.request.method == "POST":
            email = request.POST.get('email')
            recipients = SendingUser.objects.values_list('email', flat=True)
            send_mail(
                'Ваш проверочный код',
                f'Ваш код: {code}',
                f'{EMAIL_HOST_USER}'
                f"{recipients}",
                fail_silently=False,
            )

            code_user = self.request.session['verification_code']

            return render(request, 'success.html', {'message': 'Код отправлен!'})

        return render(request, 'send_code_form.html')


class AuthRegister(FormView):
    template_name = "authorization/register.html"
    form_class = AuthForm
    success_url = reverse_lazy("authorization:home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать"
        message = f"Спасибо, что зарегистрировались в нашем сервисе! Введите этот код: {code} на сайте."
        from_email = EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)



