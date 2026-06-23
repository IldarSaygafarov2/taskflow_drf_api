from django.db import models

from core.apps.common.models import BaseModel


class Comment(BaseModel):
    task = models.ForeignKey(
        "tasks.Task", on_delete=models.CASCADE, verbose_name="Task"
    )
    author = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, verbose_name="User"
    )
    content = models.TextField(verbose_name="Content")

    def __str__(self):
        return (
            f'Comment for task "{self.task.title}" from user "{self.author.username}"'
        )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
