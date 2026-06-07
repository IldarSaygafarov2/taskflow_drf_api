from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .models import Board, BoardColumn


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
    board = get_object_or_404(Board, id=board_id)

    if request.method == "GET":
        board_serializer = serializers.BoardSerializer(board, many=False)
        return Response(board_serializer.data)
    if request.method == "PATCH":
        board_update_serializer = serializers.BoardUpdateSerializer(
            board, data=request.data, partial=True
        )
        board_update_serializer.is_valid(raise_exception=True)
        updated_board = board_update_serializer.save()
        updated_board_serializer = serializers.BoardSerializer(
            updated_board, many=False
        )
        return Response(updated_board_serializer.data)

    board.delete()
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
    board = get_object_or_404(Board, id=board_id)
    if request.method == "POST":
        board_column_serializer = serializers.BoardColumnCreateSerializer(
            data=request.data, context={"board": board}
        )
        board_column_serializer.is_valid(raise_exception=True)
        new_column = board_column_serializer.save()
        column_serializer = serializers.BoardColumnSerializer(new_column)
        return Response(column_serializer.data)

    columns = board.boardcolumn_set.all()
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
    column = get_object_or_404(BoardColumn, id=column_id)
    if request.method == "GET":
        column_serializer = serializers.BoardColumnSerializer(column, many=False)
        return Response(column_serializer.data)

    if request.method == "PATCH":
        column_serializer = serializers.BoardColumnUpdateSerializer(
            column, data=request.data, partial=True
        )
        column_serializer.is_valid(raise_exception=True)
        updated_column = column_serializer.save()
        updated_column_serializer = serializers.BoardColumnSerializer(updated_column)
        return Response(updated_column_serializer.data)

    column.delete()
    return Response({"message": "Column deleted"})
