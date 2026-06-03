from django.contrib import admin
from unfold import admin as unfold_admin

from . import models


class WorkspaceMemberInline(unfold_admin.TabularInline):
    model = models.WorkspaceMember
    extra = 1


@admin.register(models.Workspace)
class WorkspaceAdmin(unfold_admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [WorkspaceMemberInline]
