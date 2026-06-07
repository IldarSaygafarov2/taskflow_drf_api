from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.apps.boards import serializers as boards_serializers
from . import serializers
from .models import Project


@swagger_auto_schema(
    method="get",
    operation_id="get_projects",
    responses={200: serializers.ProjectListSerializer},
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
        project_creation_serializer = serializers.ProjectCreateSerializer(
            data=request.data, context={"request": request}
        )
        project_creation_serializer.is_valid(raise_exception=True)
        new_project = project_creation_serializer.save()
        new_project_serializer = serializers.ProjectDetailSerializer(new_project)
        return Response(new_project_serializer.data)

    projects = Project.objects.all()
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
    project = get_object_or_404(Project, id=project_id)
    if request.method == "GET":
        serializer = serializers.ProjectDetailSerializer(project, many=False)
        return Response(serializer.data)
    if request.method == "DELETE":
        project.delete()
        return Response({"message": "Project deleted"})

    project_update_serializer = serializers.ProjectUpdateSerializer(
        project, data=request.data, partial=True
    )
    project_update_serializer.is_valid(raise_exception=True)
    updated_project = project_update_serializer.save()
    updated_project_serializer = serializers.ProjectDetailSerializer(
        updated_project, many=False
    )
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
    project = get_object_or_404(Project, id=project_id)

    if request.method == "GET":
        project_boards = project.board_set.all()
        project_boards_serializer = boards_serializers.BoardProjectSerializer(
            project_boards, many=True
        )
        return Response(project_boards_serializer.data)

    serializer = boards_serializers.BoardProjectCreateSerializer(
        data=request.data, context={"project": project}
    )
    serializer.is_valid(raise_exception=True)
    new_board = serializer.save()
    new_board_serializer = boards_serializers.BoardProjectSerializer(new_board)
    return Response(new_board_serializer.data)
