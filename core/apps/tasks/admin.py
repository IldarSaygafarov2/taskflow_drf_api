from django.contrib import admin
from unfold import admin as unfold_admin

from .models import Task


@admin.register(Task)
class TaskAdmin(unfold_admin.ModelAdmin):
    pass
