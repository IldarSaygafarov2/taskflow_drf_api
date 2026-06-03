from django.contrib import admin
from unfold import admin as unfold_admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(unfold_admin.ModelAdmin):
    pass
