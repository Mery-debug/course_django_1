from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from authorization.forms import CodeForm, AuthForm
from authorization.models import Auth
from authorization.services import random_code_generator
from config.settings import EMAIL_HOST_USER
from sending_emeil.models import SendingUser, Sending

code = next(random_code_generator())


class AccessCodeView(TemplateView):
    model = Sending
    form = CodeForm
    template_name = "authorization/access_code.html"

    def get_success_url(self):
        code_user = self.request.code
        if code_user == code:
            Auth.is_active = True
            return reverse_lazy("sending_emeil:home")
        Auth.is_active = False
        raise ValidationError("Вы ввели не верный код")


class AuthRegister(FormView):
    template_name = "authorization/registration.html"
    form_class = AuthForm
    success_url = reverse_lazy("sending_emeil:home")

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


class CustomLogoutView(TemplateView):
    template_name = "authorization/goodbye.html"
    success_url = reverse_lazy("authorization:goodbye")

    def get_success_url(self):
        return render(request, "authorization/goodbye.html")


class CustomLoginView(LoginView):
    template_name = "authorization/login.html"
    success_url = reverse_lazy("sending_emeil:home")


