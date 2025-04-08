from django import forms
from django.core.exceptions import ValidationError

from .models import Email, Sending, SendingUser


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
                    "placeholder": f"{self.fields[field_name].label.lower()}",
                }
            )


class SendingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SendingForm, self).__init__(*args, **kwargs)
        self.update_field_attributes()

    class Meta:
        model = Sending
        fields = ['mail', 'users']

    def update_field_attributes(self):
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": f"{self.fields[field_name].label.lower()}",
                }
            )


class SendingUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SendingUserForm, self).__init__(*args, **kwargs)
        self.update_field_attributes()

    class Meta:
        model = SendingUser
        fields = ['email', 'fio', 'description']

    def update_field_attributes(self):
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": f"{self.fields[field_name].label.lower()}",
                }
            )

