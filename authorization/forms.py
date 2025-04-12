import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from authorization.models import Auth


class AuthForm(UserCreationForm):
    email = forms.EmailField(help_text="Адрес почты")

    class Meta:
        model = Auth
        fields = ["email", "password1", "password2"]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            raise forms.ValidationError("Почта должна быть вида user@example.ru")
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if Auth.objects.filter(email=email).exists():
            raise ValidationError(f"Пользователь с почтой {email} уже существует.")


class CodeForm(forms.ModelForm):
    code = forms.IntegerField(max_value=9999, min_value=1000)

    class Meta:
        model = Auth
        fields = ['code']

