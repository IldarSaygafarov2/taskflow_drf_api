from .models import Workspace
from . import serializers


def get_workspaces_list():
    return Workspace.objects.all()


def create_workspace(request):
    workspace_serializer = serializers.WorkspaceCreateSerializer(
        data=request.data,
        context={"request": request},
    )
    workspace_serializer.is_valid(raise_exception=True)
    saved_workspace = workspace_serializer.save()
    return saved_workspace


def update_workspace(workspace, request):
    workspace_serializer = serializers.WorkspaceUpdateSerializer(
        workspace,
        data=request.data,
        partial=True,
    )
    workspace_serializer.is_valid(raise_exception=True)
    return workspace_serializer.save()


def add_workspace_member(workspace, request):
    serializer = serializers.WorkspaceMemberCreateSerializer(
        data=request.data,
        context={"workspace": workspace},
    )
    serializer.is_valid(raise_exception=True)
    output = serializer.save()
    return output
