from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

app_name = "authorization"

urlpatterns = [
    path("admin/", admin.site.urls),
    ]