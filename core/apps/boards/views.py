from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .services import (
    create_board_column,
    delete_board,
    delete_column,
    get_board,
    get_board_columns,
    get_board_kanban,
    get_column,
    update_board,
    update_column,
)


@swagger_auto_schema(
    method="get",
    operation_id="get_board_by_id",
    responses={200: serializers.BoardSerializer},
)
@swagger_auto_schema(
    method="patch",
    operation_id="update_board",
    request_body=serializers.BoardUpdateSerializer,
    responses={200: serializers.BoardSerializer},
)
@swagger_auto_schema(method="delete", operation_id="delete_board")
@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def get_update_delete_board(request, board_id):
    if request.method == "GET":
        board = get_board(board_id)
        board_serializer = serializers.BoardSerializer(board)
        return Response(board_serializer.data)

    if request.method == "PATCH":
        updated_board = update_board(board_id, request.data)
        updated_board_serializer = serializers.BoardSerializer(updated_board)
        return Response(updated_board_serializer.data)

    delete_board(board_id)
    return Response({"message": "Board deleted"})


@swagger_auto_schema(
    method="post",
    operation_id="create_board_column",
    request_body=serializers.BoardColumnCreateSerializer,
    responses={200: serializers.BoardColumnSerializer},
)
@swagger_auto_schema(
    method="get",
    operation_id="get_board_columns",
    responses={200: serializers.BoardColumnSerializer},
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def get_create_board_columns(request, board_id):
    if request.method == "POST":
        new_column = create_board_column(board_id, request.data)
        column_serializer = serializers.BoardColumnSerializer(new_column)
        return Response(column_serializer.data)

    columns = get_board_columns(board_id)
    columns_serializer = serializers.BoardColumnSerializer(columns, many=True)
    return Response(columns_serializer.data)


@swagger_auto_schema(
    method="get",
    operation_id="get_column",
    responses={200: serializers.BoardColumnSerializer},
)
@swagger_auto_schema(
    method="patch",
    operation_id="update_column",
    request_body=serializers.BoardColumnUpdateSerializer,
    responses={200: serializers.BoardColumnSerializer},
)
@swagger_auto_schema(method="delete", operation_id="delete_column")
@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def get_update_delete_column(request, column_id):
    if request.method == "GET":
        column = get_column(column_id)
        column_serializer = serializers.BoardColumnSerializer(column)
        return Response(column_serializer.data)

    if request.method == "PATCH":
        updated_column = update_column(column_id, request.data)
        updated_column_serializer = serializers.BoardColumnSerializer(updated_column)
        return Response(updated_column_serializer.data)

    delete_column(column_id)
    return Response({"message": "Column deleted"})


@swagger_auto_schema(
    method="get",
    operation_id="get_kanban_table",
    responses={200: serializers.BoardKanbanSerializer},
)
@api_view(["GET"])
def get_kanban(request, board_id):
    board = get_board_kanban(board_id)
    serializer = serializers.BoardKanbanSerializer(board)
    return Response(serializer.data)
