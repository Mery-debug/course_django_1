

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView

from config.settings import EMAIL_HOST_USER, MANAG_GROUP
from sending_emeil import forms, models
from sending_emeil.forms import SendingForm, SendingManagerForm
from sending_emeil.models import Sending, SendingUser, Email, SendTry


class HomeView(TemplateView):
    template_name = "sending_emeil/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count_sending"] = Sending.objects.count()
        context["count_active_sending"] = Sending.objects.filter(status="STARTED").count()
        context["unique_sendinguser"] = SendingUser.objects.count()
        return context


class SendingListView(LoginRequiredMixin, ListView):
    model = Sending
    template_name = "sending_emeil/sending_list.html"
    context_object_name = "sendings"
    login_url = "/authorization/login/"
    success_url = reverse_lazy("sending_emeil:sending_list")

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name=MANAG_GROUP).exists():
            return Sending.objects.all()
        queryset = cache.get('publish_sendings')
        if not queryset:
            queryset = Sending.objects.filter(is_publish=True)
            cache.set('publish_sendings', queryset, 60 * 15)
        return queryset


@method_decorator(cache_page(60 * 15), name='dispatch')
class SendingDetailView(DetailView):
    model = Sending
    template_name = "sending_emeil/sending_detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_detail", kwargs={"pk": self.object.pk}
        )

    def get_form_class(self):
        user = self.request.user
        if user.groups.filter(name=MANAG_GROUP).exists():
            return SendingManagerForm
        return SendingForm

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name=MANAG_GROUP).exists():
            return Sending.objects.all()
        return Sending.objects.filter(is_publish=True)


class SendingCreateView(LoginRequiredMixin, CreateView):
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


class SendingUpdateView(LoginRequiredMixin, UpdateView):
    model = Sending
    form_class = forms.SendingForm
    template_name = "sending_emeil/sending_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_detail", kwargs={"pk": self.object.pk}
        )


class SendingDeleteView(LoginRequiredMixin, DeleteView):
    model = Sending
    template_name = "sending_emeil/sending_delete.html"
    success_url = reverse_lazy("sending_emeil:sending_list")


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


class MailUpdateView(LoginRequiredMixin, UpdateView):
    model = Email
    form_class = forms.EmailForm
    template_name = "sending_emeil/mail_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:mail_detail", kwargs={"pk": self.object.pk}
        )


class MailCreateView(LoginRequiredMixin, CreateView):
    model = Email
    form_class = forms.EmailForm
    template_name = "sending_emeil/mail_create.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:mail_detail", kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        mail = form.save(commit=False)
        user = self.request.user
        mail.owner = user
        mail.save()
        return super().form_valid(form)


class MailDeleteView(LoginRequiredMixin, DeleteView):
    model = Email
    template_name = "sending_emeil/mail_delete.html"
    success_url = reverse_lazy("sending_emeil:mail_list")


class SendingUserListView(ListView):
    model = SendingUser
    template_name = "sending_emeil/sending_user_list.html"
    context_object_name = "sendingusers"
    success_url = reverse_lazy("sending_emeil:sending_user_list")


class SendingUserDetailView(LoginRequiredMixin, DetailView):
    model = SendingUser
    template_name = "sending_emeil/sending_user_detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_user_detail", kwargs={"pk": self.object.pk}
        )


class SendingUserCreateView(LoginRequiredMixin, CreateView):
    model = SendingUser
    template_name = "sending_emeil/sending_user_create.html"
    form_class = forms.SendingUserForm
    success_url = reverse_lazy("sending_emeil:sending_user_list")

    def form_valid(self, form):
        sending_user = form.save(commit=False)
        user = self.request.user
        sending_user.owner = user
        sending_user.save()
        return super().form_valid(form)


class SendingUserUpdateView(LoginRequiredMixin, UpdateView):
    model = SendingUser
    form_class = forms.SendingUserForm
    template_name = "sending_emeil/sending_user_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "sending_emeil:sending_user_update", kwargs={"pk": self.object.pk}
        )

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name=MANAG_GROUP).exists():
            return Sending.objects.all()
        queryset = cache.get('published_sending')
        if not queryset:
            queryset = Sending.objects.filter(is_published=True)
            cache.set('published_sending', queryset, 60 * 15)
        return queryset


class SendingUserDeleteView(LoginRequiredMixin, DeleteView):
    model = SendingUser
    template_name = "sending_emeil/sending_user_delete.html"
    success_url = reverse_lazy("sending_emeil:sending_user_list")


class SendTryList(ListView):
    model = SendTry
    template_name = "sending_emeil/statistic_list.html"
    context_object_name = "sendtries"
    success_url = reverse_lazy("sending_emeil:statistic_list")


class SendingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        sending = get_object_or_404(Sending, pk=pk)
        if sending.status == Sending.STOPPED:
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






