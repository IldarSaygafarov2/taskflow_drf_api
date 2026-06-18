from datetime import timedelta

from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.apps.attachments import serializers as attachment_serializers
from core.apps.attachments.models import Attachment
from core.apps.comments import serializers as comments_serializers
from core.apps.comments.models import Comment
from core.apps.common.tasks import send_message_to_email
from core.project import settings

from . import serializers
from .models import Task, TaskPriority, TaskStatus


def apply_filters(params, qs):
    if status := params.get("status"):
        qs = qs.filter(status=status)
    if priority := params.get("priority"):
        qs = qs.filter(priority=priority)
    return qs


@swagger_auto_schema(
    method="get",
    operation_id="get_all_tasks",
    responses={200: serializers.TaskSerializer},
    manual_parameters=[
        openapi.Parameter(
            "priority",
            openapi.IN_QUERY,
            description="Filter by priority",
            type=openapi.TYPE_STRING,
            enum=[item[0] for item in TaskPriority.choices],
        ),
        openapi.Parameter(
            "status",
            openapi.IN_QUERY,
            description="Filter by status",
            type=openapi.TYPE_STRING,
            enum=[item[0] for item in TaskStatus.choices],
        ),
        openapi.Parameter(
            "ordering",
            openapi.IN_QUERY,
            description="Ordering fields",
            type=openapi.TYPE_STRING,
            enum=settings.TASK_ORDERING_FIELDS,
        ),
    ],
)
@swagger_auto_schema(
    method="post",
    operation_id="create_task",
    request_body=serializers.TaskCreateSerializer,
    responses={200: serializers.TaskSerializer},
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def get_or_create_task(request):
    if request.method == "GET":
        params = request.GET
        tasks = Task.objects.all()
        tasks = apply_filters(params, tasks)
        tasks_serializer = serializers.TaskSerializer(tasks, many=True)
        return Response(tasks_serializer.data)

    serializer = serializers.TaskCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    created = serializer.save()
    notification_time = (created.deadline - timedelta(days=1)) + timedelta(minutes=5)
    print(notification_time)

    created_serializer = serializers.TaskSerializer(created)
    data = created_serializer.data
    assignee_email = data.get("assignee")["email"]
    # notify user about deadline
    deadline_message = """
The deadline for this project is approaching, hurry up.
"""
    send_message_to_email.apply_async(
        args=["Deadline is comming", deadline_message, assignee_email],
        eta=notification_time,
    )
    # send message about task created
    send_message_to_email.delay(
        subject="Task apply",
        message=f"Your task created: {created}",
        recipient=assignee_email,
    )
    return Response(data)


@swagger_auto_schema(
    method="get",
    operation_id="get_task_detail",
    responses={200: serializers.TaskDetailSerializer},
)
@swagger_auto_schema(
    method="patch",
    operation_id="update_task",
    request_body=serializers.TaskUpdateSerializer,
    responses={200: serializers.TaskDetailSerializer},
)
@swagger_auto_schema(method="delete", operation_id="delete_task")
@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def get_task_by_id(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "GET":
        detail_serializer = serializers.TaskDetailSerializer(task)
        return Response(detail_serializer.data)
    if request.method == "PATCH":
        updated_serializer = serializers.TaskUpdateSerializer(
            task, data=request.data, partial=True
        )
        updated_serializer.is_valid(raise_exception=True)
        updated_task = updated_serializer.save()
        serializer = serializers.TaskDetailSerializer(updated_task)
        return Response(serializer.data)

    task.delete()

    return Response({"message": "task deleted"})


@swagger_auto_schema(
    method="get",
    operation_id="get_all_task_comments",
    responses={200: comments_serializers.CommentSerializer},
)
@swagger_auto_schema(
    method="post",
    operation_id="create_task_comment",
    request_body=comments_serializers.CommentCreateSerializer,
    responses={200: comments_serializers.CommentSerializer},
)
@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def get_or_create_task_comments(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "GET":
        comments = task.comment_set.all()
        comments_serializer = comments_serializers.CommentSerializer(
            comments, many=True
        )
        return Response(comments_serializer.data)

    comments_serializer = comments_serializers.CommentCreateSerializer(
        data=request.data,
        context={"task": task, "request": request},
    )
    comments_serializer.is_valid(raise_exception=True)
    new_comment = comments_serializer.save()
    new_comment_serializer = comments_serializers.CommentSerializer(new_comment)
    return Response(new_comment_serializer.data)


@swagger_auto_schema(method="delete", operation_id="delete_task_comment")
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_task_comment(request, task_id, comment_id):
    _ = get_object_or_404(Task, id=task_id)
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return Response({"message": "Comment deleted"})


@swagger_auto_schema(
    method="get",
    operation_id="get_all_task_attachments",
    responses={200: attachment_serializers.AttachmentReadSerializer},
)
@swagger_auto_schema(
    method="post",
    operation_id="create_task_attachment",
    request_body=attachment_serializers.AttachmentCreateSerializer,
    responses={200: attachment_serializers.AttachmentReadSerializer},
)
@api_view(["GET", "POST"])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def get_or_create_task_attachments(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "GET":
        attachments = task.attachment_set.all()
        serializer = attachment_serializers.AttachmentReadSerializer(
            attachments, many=True
        )
        return Response(serializer.data)

    serializer = attachment_serializers.AttachmentCreateSerializer(
        data=request.data,
        context={"task": task, "request": request},
    )
    serializer.is_valid(raise_exception=True)
    new_attachment = serializer.save()
    new_attachment_serializer = attachment_serializers.AttachmentReadSerializer(
        new_attachment
    )
    return Response(new_attachment_serializer.data)


@swagger_auto_schema(method="delete", operation_id="delete_task_attachment")
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_task_attachment(request, task_id, attachment_id):
    _ = get_object_or_404(Task, id=task_id)

    attachment = get_object_or_404(Attachment, id=attachment_id)
    attachment.delete()
    return Response({"message": "Attachment deleted"})
