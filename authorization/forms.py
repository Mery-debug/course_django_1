from typing import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from authorization.models import Auth


class AuthForm(UserCreationForm):
    email = forms.EmailField(unique=True, verbose_name="Адрес почты")
    img = forms.ImageField(
        upload_to="media/img/", blank=True, null=True, verbose_name="Изображение"
    )
    country = forms.CharField(null=True, blank=True, verbose_name="Страна")
    phone_number = forms.IntegerField(
        null=True, blank=True, help_text="Номер должен содержать только цифры"
    )

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
    def __init__(self, *args, **kwargs):
        super(CodeForm, self).__init__(*args, **kwargs)
        self.update_field_attributes()

    class Meta:
        model = Auth
        fields = ['code']

    def update_field_attributes(self):
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {
                    'class': 'form-control',
                    'placeholder': f"{self.fields[field_name].label.lower()}",
                }
            )
