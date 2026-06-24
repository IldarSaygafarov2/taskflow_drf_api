from datetime import timedelta

from django.shortcuts import get_object_or_404

from core.apps.common.services import schedule_email
from core.apps.attachments.models import Attachment
from core.apps.attachments import serializers as attachment_serializers
from core.apps.comments.models import Comment
from core.apps.comments import serializers as comments_serializers

from . import serializers
from .models import Task


def apply_filters(queryset, status=None, priority=None):
    """Apply status and priority filters to task queryset."""
    if status:
        queryset = queryset.filter(status=status)
    if priority:
        queryset = queryset.filter(priority=priority)
    return queryset


def get_tasks_list(status=None, priority=None):
    """Get all tasks, optionally filtered by status and priority."""
    tasks = Task.objects.all()
    return apply_filters(tasks, status=status, priority=priority)


def create_task(task_data):
    """Create a new task and send notifications to assignee."""
    serializer = serializers.TaskCreateSerializer(data=task_data)
    serializer.is_valid(raise_exception=True)
    task = serializer.save()
    _send_task_notifications(task)
    return task


def _send_task_notifications(task):
    """Send deadline reminder and task creation emails."""
    notification_time = (task.deadline - timedelta(days=1)) + timedelta(minutes=5)

    schedule_email(
        subject="Deadline is coming",
        message="The deadline for this project is approaching, hurry up.",
        recipient=task.assignee.email,
        eta=notification_time,
    )

    schedule_email(
        subject="Task created",
        message=f"Your task created: {task.title}",
        recipient=task.assignee.email,
    )


def get_task(task_id):
    """Get a task by ID or raise 404."""
    return get_object_or_404(Task, id=task_id)


def update_task(task_id, task_data):
    """Update a task with partial data."""
    task = get_task(task_id)
    serializer = serializers.TaskUpdateSerializer(task, data=task_data, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def delete_task(task_id):
    """Delete a task by ID."""
    task = get_task(task_id)
    task.delete()


def get_task_comments(task_id):
    """Get all comments for a task."""
    task = get_task(task_id)
    return task.comment_set.all()


def create_task_comment(task_id, comment_data, request):
    """Create a new comment for a task."""
    task = get_task(task_id)
    serializer = comments_serializers.CommentCreateSerializer(
        data=comment_data,
        context={"task": task, "request": request},
    )
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def delete_task_comment(task_id, comment_id):
    """Delete a task comment."""
    _ = get_task(task_id)
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()


def get_task_attachments(task_id):
    """Get all attachments for a task."""
    task = get_task(task_id)
    return task.attachment_set.all()


def create_task_attachment(task_id, attachment_data, request):
    """Create a new attachment for a task."""
    task = get_task(task_id)
    serializer = attachment_serializers.AttachmentCreateSerializer(
        data=attachment_data,
        context={"task": task, "request": request},
    )
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def delete_task_attachment(task_id, attachment_id):
    """Delete a task attachment."""
    _ = get_task(task_id)
    attachment = get_object_or_404(Attachment, id=attachment_id)
    attachment.delete()
