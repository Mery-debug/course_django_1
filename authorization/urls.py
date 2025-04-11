from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from authorization.views import AccessCodeView, AuthRegister

app_name = "authorization"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("access_code/", AccessCodeView.as_view(), name="access_code"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registration/", AuthRegister.as_view(), name="registration"),
    ]
