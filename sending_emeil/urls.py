from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
from .views import SendingView

app_name = "sending_emeil"

urlpatterns = [
    path("sending_list/", views.SendingListView.as_view(), name="sending_list"),
    path(
        "sending_detail/<int:pk>/",
        cache_page(60)(views.SendingDetailView.as_view(template_name="sending_emeil/sending_detail.html")),
        name="sending_detail"
    ),
    path("create_sending/", views.SendingCreateView.as_view(), name="sending_create"),
    path("sending_update/<int:pk>/", views.SendingUpdateView.as_view(), name="sending_update"),
    path("sending_delete/<int:pk>/", views.SendingDeleteView.as_view(), name="sending_delete"),
    path("mail_list/", views.MailListView.as_view(), name="mail_list"),
    path(
        "mail_detail/<int:pk>/",
        cache_page(60)(views.MailDetailView.as_view(template_name="sending_emeil/mail_detail.html")),
        name="mail_detail"
    ),
    path("create_mail/", views.MailCreateView.as_view(), name="mail_create"),
    path("update_mail/<int:pk>/", views.MailUpdateView.as_view(), name="mail_update"),
    path("delete_mail/<int:pk>/", views.MailDeleteView.as_view(), name="mail_delete"),
    path("sending_user_list/", views.SendingUserListView.as_view(), name="sending_user_list"),
    path(
        "sending_user_detail/<int:pk>/",
        cache_page(60)(views.SendingUserDetailView.as_view(template_name="sending_emeil/sending_user_detail.html")),
        name="sending_user_detail"
    ),
    path("create_user_sending/", views.SendingUserCreateView.as_view(), name="sending_user_create"),
    path("sending_user_update/<int:pk>/", views.SendingUserUpdateView.as_view(), name="sending_user_update"),
    path("delete_sending_user/<int:pk>/", views.SendingUserDeleteView.as_view(), name="sending_user_delete"),
    path("statistic_list/", views.SendTryList.as_view(), name="statistic_list"),
    path("sending_post/<int:pk>/", SendingView.as_view(), name="send_sending"),
    ]
