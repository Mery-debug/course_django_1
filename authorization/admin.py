from django.contrib import admin

from authorization.models import Auth


@admin.register(Auth)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("email", "username")
    list_filter = ("email",)
    search_fields = ("email",)
