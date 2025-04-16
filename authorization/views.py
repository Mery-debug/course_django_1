from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from authorization.forms import CodeForm, AuthForm
from authorization.models import Auth, Code
from authorization.services import random_code_generator
from config.settings import EMAIL_HOST_USER
from sending_emeil.models import SendingUser, Sending

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
    success_url = reverse_lazy("auth:goodbye")

    def get_success_url(self):
        return render(request, "authorization/goodbye.html")


class CustomLoginView(LoginView):
    template_name = "authorization/login.html"
    success_url = reverse_lazy("home")


