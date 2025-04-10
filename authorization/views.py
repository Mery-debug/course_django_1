from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from authorization.models import Auth
from authorization.services import random_code


class AccessCodeView(TemplateView):
    model = Auth
    form = CodeForm
    template_name = "authorization/access_code.html"

    def get_success_url(self):
        code_user = self.request.code
        code = random_code()
        if code_user == code:
            self.is_active = True
            return reverse_lazy("sending_emeil:home")
        raise ValidationError("Вы ввели не верный код")


