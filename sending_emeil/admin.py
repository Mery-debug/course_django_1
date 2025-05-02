from django.contrib import admin

from .models import Sending, Email, SendingUser, SendTry


@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
    list_display = ("status", "mail")
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


@admin.register(SendTry)
class SendTryAdmin(admin.ModelAdmin):
    list_display = ("status", "sending")
    list_filter = ("sending",)
    search_fields = ("sending",)


