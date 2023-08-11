from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'target_user',
                    'is_read', 'timestamp', 'post', 'comment')
    list_filter = ('type', 'is_read')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email',
                     'target_user__username', 'target_user__first_name', 'target_user__last_name', 'target_user__email')
