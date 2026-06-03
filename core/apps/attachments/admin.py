from django.contrib import admin
from unfold import admin as unfold_admin

from .models import Attachment


@admin.register(Attachment)
class AttachmentAdmin(unfold_admin.ModelAdmin):
    pass
