from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.apps.attachments import serializers as attachment_serializers
from core.apps.comments import serializers as comments_serializers
from core.project import settings

from . import serializers, services
from .models import TaskPriority, TaskStatus


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
        status = request.GET.get("status")
        priority = request.GET.get("priority")
        tasks = services.get_tasks_list(status=status, priority=priority)
        tasks_serializer = serializers.TaskSerializer(tasks, many=True)
        return Response(tasks_serializer.data)

    created = services.create_task(request.data)
    created_serializer = serializers.TaskSerializer(created)
    return Response(created_serializer.data)


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
    if request.method == "GET":
        task = services.get_task(task_id)
        detail_serializer = serializers.TaskDetailSerializer(task)
        return Response(detail_serializer.data)

    if request.method == "PATCH":
        updated_task = services.update_task(task_id, request.data)
        serializer = serializers.TaskDetailSerializer(updated_task)
        return Response(serializer.data)

    services.delete_task(task_id)
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
    if request.method == "GET":
        comments = services.get_task_comments(task_id)
        comments_serializer = comments_serializers.CommentSerializer(
            comments, many=True
        )
        return Response(comments_serializer.data)

    new_comment = services.create_task_comment(task_id, request.data, request)
    new_comment_serializer = comments_serializers.CommentSerializer(new_comment)
    return Response(new_comment_serializer.data)


@swagger_auto_schema(method="delete", operation_id="delete_task_comment")
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_task_comment(request, task_id, comment_id):
    services.delete_task_comment(task_id, comment_id)
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
    if request.method == "GET":
        attachments = services.get_task_attachments(task_id)
        serializer = attachment_serializers.AttachmentReadSerializer(
            attachments, many=True
        )
        return Response(serializer.data)

    new_attachment = services.create_task_attachment(task_id, request.data, request)
    new_attachment_serializer = attachment_serializers.AttachmentReadSerializer(
        new_attachment
    )
    return Response(new_attachment_serializer.data)


@swagger_auto_schema(method="delete", operation_id="delete_task_attachment")
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_task_attachment(request, task_id, attachment_id):
    services.delete_task_attachment(task_id, attachment_id)
    return Response({"message": "Attachment deleted"})
