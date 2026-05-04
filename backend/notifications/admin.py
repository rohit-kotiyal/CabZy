from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_email', 'type', 'title', 'is_read', 'created_at']
    list_filter  = ['type', 'is_read']

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User'