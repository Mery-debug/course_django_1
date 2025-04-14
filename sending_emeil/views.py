from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page

from config.settings import EMAIL_HOST_USER
from sending_emeil import forms, models


class HomeView(generic.TemplateView):
    template_name = "sending_emeil/home.html"


class SendingListView(generic.ListView):
    model = models.Sending
    template_name = "sending_emeil/sending_list.html"
    context_object_name = "sendings"
    success_url = reverse_lazy("sending_emeil:sending_list")


@method_decorator(cache_page(60 * 15), name='dispatch')
class SendingDetailView(generic.DetailView):
    model = models.Sending
    template_name = "sending_emeil/sending_detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_detail", kwargs={"pk": self.object.pk}
        )

    def send_email(self):
        recipient_list = []
        subject = self.request.filter('subject')
        message = self.request.filter('text')
        from_email = EMAIL_HOST_USER
        for user in self.request.filter('users'):
            recipient_list.append(user)
        send_mail(subject, message, from_email, recipient_list)



class SendingCreateView(generic.CreateView):
    model = models.Sending
    form_class = forms.SendingForm
    template_name = "sending_emeil/sending_create.html"

    def get_success_url(self):
        return reverse_lazy("sending_emeil:sending_list")


class SendingUpdateView(generic.UpdateView):
    model = models.Sending
    form_class = forms.SendingForm
    template_name = "sending_emeil/sending_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_update", kwargs={"pk": self.object.pk}
        )


class SendingDeleteView(generic.DeleteView):
    model = models.Sending
    success_url = reverse_lazy("sending_emeil:sending_list")
    context_object_name = "sendings"


class MailListView(generic.ListView):
    model = models.Email
    template_name = "sending_emeil/mail_list.html"
    context_object_name = "emails"


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailDetailView(generic.DetailView):
    model = models.Email
    template_name = "sending_emeil/mail_detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:mail_detail", kwargs={"pk": self.object.pk}
        )


class MailUpdateView(generic.UpdateView):
    model = models.Email
    form_class = forms.EmailForm
    template_name = "sending_emeil/mail_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:mail_update", kwargs={"pk": self.object.pk}
        )


class MailCreateView(generic.CreateView):
    model = models.Email
    form_class = forms.EmailForm
    template_name = "sending_emeil/mail_create.html"
    success_url = reverse_lazy("sending_emeil:mail_create")


class MailDeleteView(generic.DeleteView):
    model = models.Email
    template_name = "sending_emeil/mail_delete.html"
    success_url = reverse_lazy("sending_emeil:mail_list")


class SendingUserListView(generic.ListView):
    model = models.SendingUser
    template_name = "sending_emeil/sending_user_list.html"
    context_object_name = "sendingusers"
    success_url = reverse_lazy("sending_emeil:sending_user_list")


class SendingUserDetailView(generic.DetailView):
    model = models.SendingUser
    template_name = "sending_emeil/sending_user_detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_user_detail", kwargs={"pk": self.object.pk}
        )


class SendingUserCreateView(generic.CreateView):
    model = models.SendingUser
    template_name = "sending_emeil/sending_user_create.html"
    form_class = forms.SendingUserForm
    success_url = reverse_lazy("sending_emeil:sending_user_create")


class SendingUserUpdateView(generic.UpdateView):
    model = models.SendingUser
    form_class = forms.SendingUserForm
    template_name = "sending_emeil/sending_user_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_user_update", kwargs={"pk": self.object.pk}
        )


class SendingUserDeleteView(generic.DeleteView):
    model = models.SendingUser
    template_name = "sending_emeil/sending_user_delete.html"
    success_url = reverse_lazy("sending_emeil:sending_user_delete")


