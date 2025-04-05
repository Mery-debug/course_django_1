from django.contrib import admin

from .models import Sending


@admin.register(Sending)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("mail", "status")
    list_filter = ("mail",)
    search_fields = ("mail",)
