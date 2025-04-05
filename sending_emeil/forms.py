from django import forms
from django.core.exceptions import ValidationError

from .models import Email



class EmailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.update_field_attributes()

    class Meta:
        model = Email
        fields = ['subject', 'text']

    def update_field_attributes(self):
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": f"Введите {self.fields[field_name].label.lower()}",
                }
            )