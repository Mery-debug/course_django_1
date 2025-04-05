

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView, ListView

from sending_emeil.forms import EmailForm, SendingForm
from sending_emeil.models import Sending, Email


class HomeView(TemplateView):
    template_name = "sending_emeil/home.html"


class SendingListView(ListView):
    model = Sending
    template_name = "sending_emeil/sending_list.html"
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
    template_name = "sending_emeil/create_sending.html"

    def get_success_url(self):
        return reverse_lazy("sending_emeil:sending_list")


class SendingUpdateView(UpdateView):
    model = Sending
    form_class = SendingForm
    template_name = "sending_emeil/update_sending.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_detail", kwargs={"pk": self.object.pk}
        )


class SendingDeleteView(DeleteView):
    model = Sending
    success_url = reverse_lazy("sending_emeil:sending_list")


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
    template_name = "sending_emeil/update_mail.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:mail_detail", kwargs={"pk": self.object.pk}
        )

class MailCreateView(CreateView):
    model = Email
    form_class = EmailForm
    template_name = "sending_emeil/create_mail.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:mail_detail", kwargs={"pk": self.object.pk}
        )

class MailDeleteView(DeleteView):
    model = Email
    success_url = reverse_lazy("sending_emeil:sending_list")
