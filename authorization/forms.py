import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

from authorization.models import Auth, Code


class AuthForm(UserCreationForm):
    email_address = forms.EmailField(help_text="Адрес почты")

    class Meta:
        model = Auth
        fields = ["email_address", "password1", "password2"]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number:
            raise forms.ValidationError("Номер телефона должен содержать только цифры")
        return phone_number

    def clean_email(self):
        email_address = self.cleaned_data.get("email")
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email_address):
            raise forms.ValidationError("Почта должна быть вида user@example.ru")
        return email_address

    def clean(self):
        cleaned_data = super().clean()
        email_address = cleaned_data.get("email_address")

        if Auth.objects.filter(email=email_address).exists():
            raise ValidationError(f"Пользователь с почтой {email_address} уже существует.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = f"user_{get_random_string(8)}"
        if commit:
            user.save()
        return user


class CodeForm(forms.Form):
    code = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.TextInput(attrs={
            'class': 'digit-input',
            'pattern': '[0-9]{4}',
            'placeholder': '••••'
        }),
        label='Код подтверждения',
        help_text='Введите 4-значный код из приветственного письма'
    )

    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isdigit():
            raise forms.ValidationError("Код должен содержать только цифры")
        if len(code) != 4:
            raise forms.ValidationError("Код должен содержать 4 цифры")
        return code

    class Meta:
        model = Code
        fields = ['code']


class ChangePasswordForm(UserCreationForm):
    class Meta:
        model = Auth
        fields = ["password1", "password2"]


class EmailForm(forms.Form):
    email_address = forms.EmailField(help_text="Адрес почты")

    def clean(self):
        cleaned_data = super().clean()
        email_address = cleaned_data.get("email_address")

        if Auth.objects.filter(email_address=email_address).exists():
            return email_address
        raise ValidationError(f"Пользователь с почтой {email_address} не существует. "
                              f"Введите почту, которую вы использовали при регистрации на сайте")

    class Meta:
        model = Auth
        fields = ["email_address"]



