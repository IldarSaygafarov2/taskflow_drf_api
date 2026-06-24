from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.apps.notifications.models import Notification
from core.apps.workspaces.services import (
    add_workspace_member,
    create_workspace,
    update_workspace,
)

from . import serializers
from .models import Workspace
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@swagger_auto_schema(
    method="get",
    operation_id="get_workspaces_list",
    responses={200: serializers.WorkspaceSerializer},
)
@swagger_auto_schema(
    method="post",
    operation_id="create_workspace",
    request_body=serializers.WorkspaceCreateSerializer,
    responses={200: serializers.WorkspaceSerializer},
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def get_create_workspaces(request):
    if request.method == "GET":
        workspaces = Workspace.objects.all()
        workspace_serializer = serializers.WorkspaceSerializer(workspaces, many=True)
        return Response(workspace_serializer.data)

    saved_workspace = create_workspace(request)
    workspace_output = serializers.WorkspaceSerializer(saved_workspace).data
    from core.apps.common.services import send_notification

    send_notification(
        user=request.user,
        title="Workspace",
        message="Workspace created",
        created_at=workspace_output.get("created_at"),
    )
    return Response(workspace_output)


@swagger_auto_schema(
    method="get",
    operation_id="get_workspace_detail",
    responses={200: serializers.WorkspaceDetailSerializer},
)
@swagger_auto_schema(
    method="patch",
    operation_id="partial_update_workspace",
    request_body=serializers.WorkspaceUpdateSerializer,
    responses={200: serializers.WorkspaceDetailSerializer},
)
@api_view(["GET", "DELETE", "PATCH"])
@permission_classes([IsAuthenticated])
def workspace_detail_delete_patch(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    if request.method == "GET":
        workspace_serializer = serializers.WorkspaceDetailSerializer(
            workspace, many=False
        )
        return Response(workspace_serializer.data)
    if request.method == "PATCH":
        updated = update_workspace(workspace, request)
        output = serializers.WorkspaceDetailSerializer(updated)
        return Response(output.data)

    workspace.delete()
    return Response({"status": "ok"})


@swagger_auto_schema(
    method="get",
    operation_id="get_workspace_members",
    responses={200: serializers.WorkspaceMemeberSerializer},
)
@swagger_auto_schema(
    method="post",
    request_body=serializers.WorkspaceMemberCreateSerializer,
    operation_id="add_member_to_workspace",
    responses={200: serializers.WorkspaceMemeberSerializer},
)
@api_view(["GET", "POST"])
def get_or_create_workspace_members(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)

    if request.method == "GET":
        members = workspace.workspacemember_set.all()
        members_serializer = serializers.WorkspaceMemeberSerializer(members, many=True)
        return Response(members_serializer.data)

    output = add_workspace_member(workspace, request)
    output = serializers.WorkspaceMemeberSerializer(output)
    return Response(output.data)
