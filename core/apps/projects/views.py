from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from . import models, serializers


@swagger_auto_schema(method="get", operation_id="get_projects")
@swagger_auto_schema(method="post", operation_id="create_project")
@api_view(["GET", "POST"])
def get_or_create_project(request):
    pass


@swagger_auto_schema(method="get", operation_id="get_project_detail")
@api_view(["GET"])
def get_project_detail(request, project_id):
    pass


@swagger_auto_schema(method="patch", operation_id="partial_update_project")
@api_view(["PATCH"])
def update_project(request, project_id):
    pass


@swagger_auto_schema(method="delete", operation_id="delete_project")
@api_view(["DELETE"])
def delete_project(request, project_id):
    pass


@swagger_auto_schema(method="get", operation_id="get_project_boards")
@swagger_auto_schema(method="post", operation_id="create_project_board")
@api_view(["GET", "POST"])
def get_create_project_boards(request, project_id):
    pass
