from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .models import Workspace, WorkspaceMember


@swagger_auto_schema(method="get", operation_id="get_workspaces_list")
@swagger_auto_schema(method="post", operation_id="create_workspace")
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def get_create_workspaces(request):
    return Response("hello")


@swagger_auto_schema(method="get", operation_id="get_workspace_detail")
@api_view(["GET"])
def get_workspace_detail(request, workspace_id):
    pass


@swagger_auto_schema(method="patch", operation_id="partial_update_workspace")
@api_view(["PATCH"])
def partial_update_workspace(request, workspace_id):
    pass


@swagger_auto_schema(method="delete", operation_id="delete_workspace")
@api_view(["DELETE"])
def delete_workspace(request, workspace_id):
    pass
