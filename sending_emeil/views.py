

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.views.decorators.cache import cache_page

from config.settings import EMAIL_HOST_USER
from sending_emeil import forms, models
from sending_emeil.models import Sending, SendingUser, Email, SendTry


class HomeView(generic.TemplateView):
    template_name = "sending_emeil/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count_sending"] = Sending.objects.count()
        context["count_active_sending"] = Sending.objects.filter(status="STARTED").count()
        context["unique_sendinguser"] = SendingUser.objects.count()
        return context


class SendingListView(generic.ListView):
    model = Sending
    template_name = "sending_emeil/sending_list.html"
    context_object_name = "sendings"
    success_url = reverse_lazy("sending_emeil:sending_list")


@method_decorator(cache_page(60 * 15), name='dispatch')
class SendingDetailView(generic.DetailView):
    model = Sending
    template_name = "sending_emeil/sending_detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_detail", kwargs={"pk": self.object.pk}
        )


class SendingCreateView(generic.CreateView):
    model = Sending
    form_class = forms.SendingForm
    template_name = "sending_emeil/sending_create.html"

    def get_success_url(self):
        return reverse_lazy("sending_emeil:sending_list")

    def form_valid(self, form):
        sending = form.save(commit=False)
        user = self.request.user
        sending.owner = user
        sending.save()
        return super().form_valid(form)


class SendingUpdateView(generic.UpdateView):
    model = Sending
    form_class = forms.SendingForm
    template_name = "sending_emeil/sending_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_update", kwargs={"pk": self.object.pk}
        )


class SendingDeleteView(generic.DeleteView):
    model = Sending
    template_name = "sending_emeil/sending_delete.html"
    success_url = reverse_lazy("sending_emeil:sending_list")


class MailListView(generic.ListView):
    model = Email
    template_name = "sending_emeil/mail_list.html"
    context_object_name = "emails"


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailDetailView(generic.DetailView):
    model = Email
    template_name = "sending_emeil/mail_detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:mail_detail", kwargs={"pk": self.object.pk}
        )


class MailUpdateView(generic.UpdateView):
    model = Email
    form_class = forms.EmailForm
    template_name = "sending_emeil/mail_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:mail_update", kwargs={"pk": self.object.pk}
        )


class MailCreateView(generic.CreateView):
    model = Email
    form_class = forms.EmailForm
    template_name = "sending_emeil/mail_create.html"
    success_url = reverse_lazy("sending_emeil:mail_create")


class MailDeleteView(generic.DeleteView):
    model = Email
    template_name = "sending_emeil/mail_delete.html"
    success_url = reverse_lazy("sending_emeil:mail_list")


class SendingUserListView(generic.ListView):
    model = SendingUser
    template_name = "sending_emeil/sending_user_list.html"
    context_object_name = "sendingusers"
    success_url = reverse_lazy("sending_emeil:sending_user_list")


class SendingUserDetailView(generic.DetailView):
    model = SendingUser
    template_name = "sending_emeil/sending_user_detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_user_detail", kwargs={"pk": self.object.pk}
        )


class SendingUserCreateView(generic.CreateView):
    model = SendingUser
    template_name = "sending_emeil/sending_user_create.html"
    form_class = forms.SendingUserForm
    success_url = reverse_lazy("sending_emeil:sending_user_create")


class SendingUserUpdateView(generic.UpdateView):
    model = SendingUser
    form_class = forms.SendingUserForm
    template_name = "sending_emeil/sending_user_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_user_update", kwargs={"pk": self.object.pk}
        )


class SendingUserDeleteView(generic.DeleteView):
    model = SendingUser
    template_name = "sending_emeil/sending_user_delete.html"
    success_url = reverse_lazy("sending_emeil:sending_user_delete")


class SendTryList(generic.ListView):
    model = SendTry
    template_name = "sending_emeil/statistic_list.html"
    context_object_name = "sendtries"
    success_url = reverse_lazy("sending_emeil:statistic_list")


class SendingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        sending = get_object_or_404(Sending, pk=pk)
        if sending.status == Sending.COMPLETED:
            return HttpResponseForbidden(f"Рассылка не может быть отправлена, так как её статус {sending.status}")
        if sending.status == Sending.CREATED:
            sending.status = Sending.STARTED
            sending.date_of_try = timezone.now()
            sending.save()
            for user in sending.users.all():
                tries = SendTry(sending=sending)
                try:
                    send_mail(
                        sending.mail.subject,
                        sending.mail.text,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                    tries.status = SendTry.SUCCESS
                    tries.answer_server = "Письмо отправлено успешно."
                except Exception as e:
                    tries.status = SendTry.FAILURE
                    tries.answer_server = str(e)
                tries.save()
            sending.status = Sending.COMPLETED
            sending.end_sending = timezone.now()
            sending.save()
        sending_stat = SendTry.objects.filter(sending=sending)
        return render(
            request, "sending_emeil/statistic_list.html", {"sending": sending, "sending_try": sending_stat}
        )






