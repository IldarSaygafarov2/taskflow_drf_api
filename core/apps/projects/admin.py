from django.contrib import admin

from unfold import admin as unfold_admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(unfold_admin.ModelAdmin):
    pass
