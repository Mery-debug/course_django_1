from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from authorization.forms import CodeForm, AuthForm, ChangePasswordForm, EmailForm
from authorization.models import Auth, Code
from authorization.services import random_code_generator
from config.settings import EMAIL_HOST_USER
from sending_emeil.models import SendingUser, Sending
import secrets

code = next(random_code_generator())


class AccessCodeView(FormView):
    template_name = "authorization/access_code.html"
    form_class = CodeForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        entered_code = form.cleaned_data['code']

        if Code.objects.filter(code=entered_code).exists():
            Auth.is_auth = True
            return super().form_valid(form)
        else:
            form.add_error(None, "Неверный код доступа")
            return self.form_invalid(form)


class AuthRegister(FormView):
    model = Auth
    template_name = "authorization/registration.html"
    form_class = AuthForm

    def get_success_url(self):
        return reverse_lazy("auth:access_code")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email_address)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать"
        message = f"Спасибо, что зарегистрировались в нашем сервисе! Введите этот код: {code} на сайте."
        from_email = EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)

    def get_auth(self):
        code_user = self.request.POST('code')
        user = self.request.user
        if code_user == code:
            user.is_auth = True
        return user


class CustomLogoutView(TemplateView):
    template_name = "authorization/goodbye.html"
    success_url = reverse_lazy("auth:goodbye")

    def get_success_url(self):
        return render(request, "authorization/goodbye.html")


class CustomLoginView(LoginView):
    template_name = "authorization/login.html"
    success_url = reverse_lazy("home")


class SendEmailView(FormView):
    model = Auth
    form_class = EmailForm
    template_name = "authorization/email_for_change_password.html"
    success_url = reverse_lazy("authorization:change_password")

    def send_email(self, form):
        user = form.save()
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/authorization/change_password/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для смены пароля {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email_address],
        )
        return super().form_valid(form)


class ChangePasswordView(FormView):
    template_name = "authorization/change_password.html"
    form_class = EmailForm
    success_url = reverse_lazy("home")



