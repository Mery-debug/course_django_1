import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

from authorization.models import Auth, Code


class AuthForm(UserCreationForm):
    email = forms.EmailField(help_text="Адрес почты")
    img = forms.ImageField(required=False, help_text="Аватар")
    phone_number = forms.IntegerField(required=False, help_text="Номер телефона")
    country = forms.CharField(required=False, help_text="Ваша страна")
    username = forms.CharField(required=True, help_text="Имя пользователя")

    class Meta:
        model = Auth
        fields = ["email", "password1", "password2"]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number:
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

