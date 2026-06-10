from django.core.mail import send_mail

from core.project import celery_app
from core.project.settings import DEFAULT_FROM_EMAIL


@celery_app.task
def send_welcome_message_to_email(subject, message, recipient):
    return send_mail(
        subject=subject,
        message=message,
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        fail_silently=False,
    )
