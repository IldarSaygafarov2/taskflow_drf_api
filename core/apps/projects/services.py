from django.shortcuts import get_object_or_404

from core.apps.boards.services import create_default_columns
from core.apps.boards import serializers as boards_serializers

from . import serializers
from .models import Project


def get_projects_list(status=None):
    """Get all projects, optionally filtered by status."""
    if status:
        return Project.objects.filter(status=status)
    return Project.objects.all()


def create_project(request):
    """Create a new project from request data."""
    serializer = serializers.ProjectCreateSerializer(
        data=request.data, context={"request": request}
    )
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def get_project(project_id):
    """Get a project by ID or raise 404."""
    return get_object_or_404(Project, id=project_id)


def delete_project(project_id):
    """Delete a project by ID."""
    project = get_project(project_id)
    project.delete()


def update_project(project_id, request_data):
    """Update a project with partial data."""
    project = get_project(project_id)
    serializer = serializers.ProjectUpdateSerializer(
        project, data=request_data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def get_project_boards(project_id):
    """Get all boards for a project."""
    project = get_project(project_id)
    return project.board_set.all()


def create_project_board(project_id, board_data):
    """Create a new board for a project and initialize default columns."""
    project = get_project(project_id)
    serializer = boards_serializers.BoardProjectCreateSerializer(
        data=board_data, context={"project": project}
    )
    serializer.is_valid(raise_exception=True)
    board = serializer.save()
    create_default_columns(board)
    return board
