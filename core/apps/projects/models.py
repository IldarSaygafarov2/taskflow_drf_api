from django.db import models

from core.apps.common.models import BaseModel


class ProjectStatus(models.TextChoices):
    ACTIVE = "active"
    ARCHIVED = "archived"
    COMPLETED = "completed"


class Project(BaseModel):
    workspace = models.ForeignKey(
        "workspaces.Workspace", on_delete=models.CASCADE, verbose_name="Workspace"
    )
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(verbose_name="description")
    status = models.CharField(
        verbose_name="status",
        choices=ProjectStatus.choices,
        default=ProjectStatus.ACTIVE,
    )
    start_date = models.DateField(verbose_name="start date")
    end_date = models.DateField(verbose_name="end date")
    created_by = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, verbose_name="Created by"
    )

    def __str__(self):
        return f"{self.workspace.name} - {self.name}"

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
