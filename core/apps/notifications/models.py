from django.db import models

from core.apps.common.models import BaseModel


class Notification(BaseModel):
    user = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, verbose_name="User"
    )
    title = models.CharField(verbose_name="Title", max_length=255)
    message = models.TextField(verbose_name="Message")
    is_read = models.BooleanField(verbose_name="Is read", default=False)

    def __str__(self):
        return f'Notification message "{self.title}" to user "{self.user.username}"'

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
