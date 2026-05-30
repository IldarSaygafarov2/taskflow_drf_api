from django.db import models

from core.apps.common.models import BaseModel


def make_task_file_upload_path(instance: "Attachment", filename: str):
    return f"tasks/{instance.task.id}/files/{filename}"


class Attachment(BaseModel):
    task = models.ForeignKey(
        "tasks.Task", on_delete=models.CASCADE, verbose_name="Task"
    )
    file = models.FileField(
        verbose_name="File", upload_to=make_task_file_upload_path, null=True, blank=True
    )
    uploaded_by = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, verbose_name="Uploaded by"
    )

    def __str__(self):
        return f'File for task "{self.task.title}" from users "{self.uploaded_by.username}"'

    class Meta:
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"
