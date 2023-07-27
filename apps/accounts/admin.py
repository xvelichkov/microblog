from django.contrib import admin

from .models import AccountUser, Notification

@admin.register(AccountUser)
class AccountUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass