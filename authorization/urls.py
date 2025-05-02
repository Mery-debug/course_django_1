from django.contrib.auth.views import LogoutView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy

from authorization.views import AccessCodeView, AuthRegister, CustomLoginView, CustomLogoutView, \
    CustomPasswordResetView, CustomPasswordResetCompleteView

app_name = "authorization"

urlpatterns = [
    path("access_code/", AccessCodeView.as_view(), name="access_code"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path(
        "logout/", LogoutView.as_view(next_page="authorization:goodbye"), name="logout"
    ),
    path(
        "password-reset/",
        CustomPasswordResetView.as_view(
            template_name="authorization/password_reset_form.html",
            email_template_name="authorization/password_reset_email.html",
            subject_template_name="authorization/password_reset_subject.txt",
            html_email_template_name="authorization/password_reset_email.html",
            extra_email_context={'site_name': 'ВашСайт'}
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(template_name="authorization/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="authorization/password_reset_confirm.html",
            success_url=reverse_lazy("authorization:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "goodbye/",
        CustomLogoutView.as_view(template_name="authorization/goodbye.html"),
        name="goodbye",
    ),
    path("registration/", AuthRegister.as_view(), name="registration"),
    ]
