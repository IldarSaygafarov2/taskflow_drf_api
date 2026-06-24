from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.apps.boards import serializers as boards_serializers
from drf_yasg import openapi

from . import serializers
from .models import ProjectStatus
from .services import (
    create_project,
    create_project_board,
    delete_project,
    get_project,
    get_project_boards,
    get_projects_list,
    update_project,
)


@swagger_auto_schema(
    method="get",
    operation_id="get_projects",
    responses={200: serializers.ProjectListSerializer},
    manual_parameters=[
        openapi.Parameter(
            "status",
            openapi.IN_QUERY,
            description="Filter by status",
            type=openapi.TYPE_STRING,
            enum=[choice[0] for choice in ProjectStatus.choices],
        ),
    ],
)
@swagger_auto_schema(
    method="post",
    operation_id="create_project",
    request_body=serializers.ProjectCreateSerializer,
    responses={200: serializers.ProjectDetailSerializer},
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def get_or_create_project(request):
    if request.method == "POST":
        new_project = create_project(request)
        new_project_serializer = serializers.ProjectDetailSerializer(new_project)
        return Response(new_project_serializer.data)

    status = request.GET.get("status")
    projects = get_projects_list(status=status)
    serializer = serializers.ProjectListSerializer(projects, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="get",
    operation_id="get_project_detail",
    responses={200: serializers.ProjectDetailSerializer},
)
@swagger_auto_schema(method="delete", operation_id="delete_project")
@swagger_auto_schema(
    method="patch",
    operation_id="partial_update_project",
    request_body=serializers.ProjectUpdateSerializer,
    responses={200: serializers.ProjectDetailSerializer},
)
@api_view(["GET", "DELETE", "PATCH"])
@permission_classes([IsAuthenticated])
def get_delete_update_project(request, project_id):
    if request.method == "GET":
        project = get_project(project_id)
        serializer = serializers.ProjectDetailSerializer(project)
        return Response(serializer.data)

    if request.method == "DELETE":
        delete_project(project_id)
        return Response({"message": "Project deleted"})

    updated_project = update_project(project_id, request.data)
    updated_project_serializer = serializers.ProjectDetailSerializer(updated_project)
    return Response(updated_project_serializer.data)


@swagger_auto_schema(
    method="get",
    operation_id="get_project_boards",
    responses={200: boards_serializers.BoardProjectSerializer},
)
@swagger_auto_schema(
    method="post",
    operation_id="create_project_board",
    request_body=boards_serializers.BoardProjectCreateSerializer,
    responses={200: boards_serializers.BoardProjectSerializer},
)
@api_view(["GET", "POST"])
def get_create_project_boards(request, project_id):
    if request.method == "GET":
        project_boards = get_project_boards(project_id)
        project_boards_serializer = boards_serializers.BoardProjectSerializer(
            project_boards, many=True
        )
        return Response(project_boards_serializer.data)

    board = create_project_board(project_id, request.data)
    new_board_serializer = boards_serializers.BoardProjectSerializer(board)
    return Response(new_board_serializer.data)
