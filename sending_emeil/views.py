from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView, ListView

from sending_emeil.forms import EmailForm, SendingForm, SendingUserForm
from sending_emeil.models import Sending, Email, SendingUser


class HomeView(TemplateView):
    template_name = "sending_emeil/home.html"


class SendingListView(ListView):
    model = Sending
    template_name = "sending_emeil/sending_list.html"
    context_object_name = "sendings"
    success_url = reverse_lazy("sending_emeil:sending_list")


@method_decorator(cache_page(60 * 15), name='dispatch')
class SendingDetailView(DetailView):
    model = Sending
    template_name = "sending_emeil/sending_detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_detail", kwargs={"pk": self.object.pk}
        )


class SendingCreateView(CreateView):
    model = Sending
    form_class = SendingForm
    template_name = "sending_emeil/sending_create.html"

    def get_success_url(self):
        return reverse_lazy("sending_emeil:sending_list")


class SendingUpdateView(UpdateView):
    model = Sending
    form_class = SendingForm
    template_name = "sending_emeil/sending_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_detail", kwargs={"pk": self.object.pk}
        )


class SendingDeleteView(DeleteView):
    model = Sending
    success_url = reverse_lazy("sending_emeil:sending_list")
    context_object_name = "sendings"


class MailListView(ListView):
    model = Email
    template_name = "sending_emeil/mail_list.html"
    context_object_name = "emails"


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailDetailView(DetailView):
    model = Email
    template_name = "sending_emeil/mail_detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:mail_detail", kwargs={"pk": self.object.pk}
        )


class MailUpdateView(UpdateView):
    model = Email
    form_class = EmailForm
    template_name = "sending_emeil/mail_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:mail_detail", kwargs={"pk": self.object.pk}
        )


class MailCreateView(CreateView):
    model = Email
    form_class = EmailForm
    template_name = "sending_emeil/mail_create.html"
    success_url = "sending_emeil:mail_create"


class MailDeleteView(DeleteView):
    model = Email
    template_name = "sending_emeil/mail_delete.html"
    success_url = reverse_lazy("sending_emeil:mail_list")


class SendingUserListView(ListView):
    model = SendingUser
    template_name = "sending_emeil/sending_user_list.html"
    context_object_name = "sending_users"
    success_url = reverse_lazy("sending_emeil:sending_user_list")


class SendingUserDetailView(DetailView):
    model = SendingUser
    template_name = "sending_emeil/sending_user_detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_detail", kwargs={"pk": self.object.pk}
        )


class SendingUserCreateView(CreateView):
    model = SendingUser
    template_name = "sending_emeil/sending_user_create.html"
    form_class = SendingUserForm
    success_url = "sending_emeil:sending_user_create"


class SendingUserUpdateView(UpdateView):
    model = SendingUser
    form_class = SendingUserForm
    template_name = "sending_emeil/sending_user_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_user_update", kwargs={"pk": self.object.pk}
        )


class SendingUserDeleteView(DeleteView):
    model = SendingUser
    template_name = "sending_emeil/sending_user_delete.html"
    success_url = reverse_lazy("sending_emeil:sending_user_delete")


