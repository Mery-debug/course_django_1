from django.contrib import admin

from .models import Sending, Email, SendingUser


@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
    list_display = ("mail", "status")
    list_filter = ("mail",)
    search_fields = ("mail",)


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("subject", "text")
    list_filter = ("subject",)
    search_fields = ("subject",)


@admin.register(SendingUser)
class SendingUserAdmin(admin.ModelAdmin):
    list_display = ("email", "fio")
    list_filter = ("email",)
    search_fields = ("email",)

