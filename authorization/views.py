from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import TemplateView, FormView

from authorization.forms import CodeForm, AuthForm, EmailForm
from authorization.models import Auth, Code
from authorization.services import random_code_generator
from config import settings
from config.settings import EMAIL_HOST_USER
import secrets

gen = random_code_generator()


class AuthRegister(FormView):
    template_name = "authorization/registration.html"
    form_class = AuthForm
    success_url = reverse_lazy("auth:access_code")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        confirmation_code = str(gen)

        Code.objects.create(
            user=user,
            code=confirmation_code
        )

        self.send_confirmation_email(user.email_address, confirmation_code)

        self.request.session['email_to_confirm'] = user.email_address
        return super().form_valid(form)

    def send_confirmation_email(self, email, confirmation_code):
        subject = "Подтверждение регистрации"
        message = f"Ваш код подтверждения: {confirmation_code}"
        from_email = EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)


class AccessCodeView(FormView):
    template_name = "authorization/access_code.html"
    form_class = CodeForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        email = self.request.session.get('email_to_confirm')
        if not email:
            form.add_error(None, "Сессия истекла, начните регистрацию заново")
            return self.form_invalid(form)

        entered_code = form.cleaned_data['code']

        try:
            user = Auth.objects.get(email_address=email)

            code_obj = Code.objects.get(
                user=user,
                code=entered_code,
                is_used=False
            )

            user.is_active = True
            user.save()

            code_obj.is_used = True
            code_obj.save()

            return super().form_valid(form)

        except Auth.DoesNotExist:
            form.add_error(None, "Пользователь не найден")
            return self.form_invalid(form)
        except Code.DoesNotExist:
            form.add_error('code', "Неверный код подтверждения")
            return self.form_invalid(form)


class CustomLogoutView(TemplateView):
    template_name = "authorization/goodbye.html"
    success_url = reverse_lazy("auth:goodbye")

    def get_success_url(self):
        return render(request, "authorization/goodbye.html")


class CustomLoginView(LoginView):
    template_name = "authorization/login.html"
    success_url = reverse_lazy("home")


class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('authorization:password_reset_done')
    success_message = "Письмо отправлено. Проверьте вашу почту"

    def form_valid(self, form):
        email = form.cleaned_data['email']

        try:
            user = Auth.objects.get(email_address=email)
        except Auth.DoesNotExist:
            return HttpResponseServerError("User not found")

        token = secrets.token_hex(16)
        user.password_reset_token = token
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        host = self.request.get_host()
        url = f"http://{host}/authorization/password-reset/{uid}/{token}/"

        try:
            send_mail(
                subject="Восстановление пароля",
                message=f"Для восстановления пароля перейдите по ссылке: {url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
            )
            return super().form_valid(form)
        except Exception as e:
            print(f"Ошибка отправки: {str(e)}")
            return HttpResponseServerError("Email error")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "authorization/password_reset_complete.html"
    success_url = reverse_lazy("authorization:login")


