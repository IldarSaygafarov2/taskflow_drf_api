from django.contrib import admin
from unfold import admin as unfold_admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(unfold_admin.ModelAdmin):
    pass
