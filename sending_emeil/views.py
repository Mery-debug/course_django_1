from msilib.schema import ListView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView

from sending_emeil.models import Sending, Email


class HomeView(TemplateView):
    template_name = "sending_emeil/home.html"


class MailListView(ListView):
    model = Sending
    context_object_name = "sendings"
    template_name = "sending_emeil/mail_list.html"
    success_url = reverse_lazy("sending_emeil:mail_list")


@method_decorator(cache_page(60 * 15), name='dispatch')
class SendingDetailView(DetailView):
    model = Sending
    template_name = "sending_emeil/mail_detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:mail_detail", kwargs={"pk": self.object.pk}
        )


class MailCreateView(CreateView):
    model = Email
    form_class = EmailForm
    template_name = "sending_emeil/create_mail.html"

    def get_success_url(self):
        return reverse_lazy("sending_emeil:mail_list")


class MailUpdateView(UpdateView):
    model = Email
    form_class = EmailForm
    template_name = "sending_emeil/update_mail.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:mail_detail", kwargs={"pk": self.object.pk}
        )


class MailDeleteView(DeleteView):
    model = Email
    success_url = reverse_lazy("sending_emeil:mail_list")



