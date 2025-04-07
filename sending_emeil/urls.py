from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    SendingDetailView,
    SendingListView,
    SendingCreateView,
    SendingUpdateView,
    SendingDeleteView,
    MailDetailView,
    MailUpdateView,
    MailCreateView,
    MailDeleteView, MailListView
)

app_name = "sending_emeil"

urlpatterns = [
    path("sending_list/", SendingListView.as_view(), name="sending_list"),
    path(
        "sending_detail/<int:pk>/",
        cache_page(60)(SendingDetailView.as_view(template_name="sending_emeil/sending_detail.html")),
        name="sending_detail"
    ),
    path("create_sending/", SendingCreateView.as_view(), name="sending_create"),
    path("update_sending/<int:pk>/", SendingUpdateView.as_view(), name="sending_update"),
    path("delete_sending/<int:pk>/", SendingDeleteView.as_view(), name="sending_delete"),
    path("mail_list/", MailListView.as_view(), name="mail_list"),
    path(
        "mail_detail/<int:pk>/",
        cache_page(60)(MailDetailView.as_view(template_name="sending_emeil/mail_detail.html")),
        name="mail_detail"
    ),
    path("create_mail/", MailCreateView.as_view(), name="mail_create"),
    path("update_mail/<int:pk>/", MailUpdateView.as_view(), name="mail_update"),
    path("delete_mail/<int:pk>/", MailDeleteView.as_view(), name="mail_delete"),
    ]
