from django.contrib import admin

from authorization.models import Auth


@admin.register(Auth)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("email_address", "username")
    list_filter = ("email_address",)
    search_fields = ("email_address",)
