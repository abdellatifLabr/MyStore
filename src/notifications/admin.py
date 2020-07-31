from django.contrib import admin

from .models import Client, NotificationType, Notification

admin.site.register(Client)
admin.site.register(Notification)
admin.site.register(NotificationType)
