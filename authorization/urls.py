from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from authorization.views import AccessCodeView, AuthRegister, CustomLoginView, CustomLogoutView

app_name = "authorization"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("access_code/", AccessCodeView.as_view(), name="access_code"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path(
        "logout/", LogoutView.as_view(next_page="authorization:goodbye"), name="logout"
    ),
    path(
        "goodbye/",
        CustomLogoutView.as_view(template_name="authorization/goodbye.html"),
        name="goodbye",
    ),
    path("registration/", AuthRegister.as_view(), name="registration"),
    ]
