from django.contrib import admin

from .models import Sending, Email


@admin.register(Sending)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("mail", "status")
    list_filter = ("mail",)
    search_fields = ("mail",)


@admin.register(Email)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("subject", "text")
    list_filter = ("subject",)
    search_fields = ("subject",)
