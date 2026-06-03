from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from .models import Task
from . import serializers
from rest_framework.decorators import api_view


@swagger_auto_schema(method="get", operation_id="get_all_tasks")
@swagger_auto_schema(method="post", operation_id="create_task")
@api_view(["GET", "POST"])
def get_or_create_task(request):
    pass


@swagger_auto_schema(method="get", operation_id="get_task_detail")
@api_view(["GET"])
def get_task_by_id(request, task_id):
    pass


@swagger_auto_schema(method="patch", operation_id="update_task")
@api_view(["PATCH"])
def partial_update_task(request, task_id):
    pass


@swagger_auto_schema(method="delete", operation_id="delete_task")
@api_view(["DELETE"])
def delete_task(request, task):
    pass


@swagger_auto_schema(method="get", operation_id="get_all_task_comments")
@swagger_auto_schema(method="post", operation_id="create_task_comment")
@api_view(["POST", "GET"])
def get_or_create_task_comments(request, task_id):
    pass


@swagger_auto_schema(method="delete", operation_id="delete_task_comment")
@api_view(["DELETE"])
def delete_task_comment(request, task_id, comment_id):
    pass
