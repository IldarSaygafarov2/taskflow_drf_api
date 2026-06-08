from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.apps.attachments import serializers as attachment_serializers
from core.apps.comments import serializers as comments_serializers

from . import serializers
from .models import Task


@swagger_auto_schema(
    method="get",
    operation_id="get_all_tasks",
    responses={200: serializers.TaskSerializer},
)
@swagger_auto_schema(
    method="post",
    operation_id="create_task",
    request_body=serializers.TaskCreateSerializer,
    responses={200: serializers.TaskSerializer},
)
@api_view(["GET", "POST"])
def get_or_create_task(request):
    if request.method == "GET":
        tasks = Task.objects.all()
        tasks_serializer = serializers.TaskSerializer(tasks, many=True)
        return Response(tasks_serializer.data)

    serializer = serializers.TaskCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    created = serializer.save()
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
def delete_task_comment(request, task_id, comment_id):
    pass


@swagger_auto_schema(method="get", operation_id="get_all_task_attachments")
@swagger_auto_schema(method="post", operation_id="create_task_attachment")
@api_view(["GET", "POST"])
def get_or_create_task_attachments(request, task_id):
    pass


@swagger_auto_schema(method="delete", operation_id="delete_task_attachment")
@api_view(["DELETE"])
def delete_task_attachment(request, task_id, attachment_id):
    pass
