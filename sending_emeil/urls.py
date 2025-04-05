from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    SendingDetailView,
    MailListView,
    MailCreateView,
    MailUpdateView,
    MailDeleteView,
    HomeView
)

app_name = "sending_emeil"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "mail_list/", MailListView.as_view(template_name="sending_emeil/mail_list.html"), name="mail_list"
    ),
    path(
        "mail_detail/<int:pk>/", SendingDetailView.as_view(template_name="sending_emeil/mail_detail.html"), name="mail_detail"
    ),
    path(
        "create/", MailCreateView.as_view(template_name="sending_emeil/create_mail.html"), name="mail_create"
    ),
    path(
        "update/<int:pk>/", MailUpdateView.as_view(template_name="sending_emeil/update_mail.html"), name="mail_update"
    ),
    path(
        "delete/<int:pd>/", MailDeleteView.as_view(template_name="sending_emeil/confirm_delete.html"), name="mail_delete"
    ),
    ]
