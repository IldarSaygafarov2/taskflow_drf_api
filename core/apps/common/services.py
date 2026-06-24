from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from core.apps.notifications.models import Notification
from core.apps.common.tasks import send_message_to_email


def delete_object_photo(photo_path: str):
    pass


def send_notification(
    user,
    title: str,
    message: str,
    created_at=None,
    group_name="notifications",
):
    notification = Notification.objects.create(user=user, title=title, message=message)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",
            "message": message,
            "title": title,
            "created_at": created_at or notification.created_at,
        },
    )
    return notification


def schedule_email(subject: str, message: str, recipient: str, eta=None):
    if eta is None:
        return send_message_to_email.delay(
            subject=subject, message=message, recipient=recipient
        )
    return send_message_to_email.apply_async(
        args=[subject, message, recipient],
        eta=eta,
    )
