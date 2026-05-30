from django.db import models

from core.apps.common.models import BaseModel


class WorkspaceMemberRole(models.TextChoices):
    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"
    GUEST = "guest"


class Workspace(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Workspace name")
    slug = models.SlugField(max_length=265, unique=True, verbose_name="Workspace slug")
    description = models.TextField(verbose_name="Workspace description")
    owner = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, verbose_name="Workspace owner"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Workspace"
        verbose_name_plural = "Workspaces"


class WorkspaceMember(BaseModel):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, verbose_name="Workspace member"
    )
    user = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, verbose_name="Workspace user"
    )
    role = models.CharField(
        choices=WorkspaceMemberRole.choices,
        max_length=255,
        verbose_name="Workspace role",
    )

    def __str__(self):
        return f"{self.workspace.name}: {self.user.username}"

    class Meta:
        verbose_name = "Workspace member"
        verbose_name_plural = "Workspace members"
