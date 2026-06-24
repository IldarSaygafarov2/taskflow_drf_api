from django.shortcuts import get_object_or_404

from core.apps.tasks.models import TaskStatus

from . import serializers
from .models import Board, BoardColumn


def create_default_columns(board):
    task_status_choices = [choice[0] for choice in TaskStatus.choices]

    for idx, choice in enumerate(task_status_choices, start=1):
        BoardColumn.objects.create(board=board, name=choice.upper(), position=idx)


def get_board(board_id):
    """Get a board by ID or raise 404."""
    return get_object_or_404(Board, id=board_id)


def update_board(board_id, request_data):
    """Update a board with partial data."""
    board = get_board(board_id)
    serializer = serializers.BoardUpdateSerializer(
        board, data=request_data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def delete_board(board_id):
    """Delete a board by ID."""
    board = get_board(board_id)
    board.delete()


def get_board_columns(board_id):
    """Get all columns for a board."""
    board = get_board(board_id)
    return board.boardcolumn_set.all()


def create_board_column(board_id, column_data):
    """Create a new column for a board."""
    board = get_board(board_id)
    serializer = serializers.BoardColumnCreateSerializer(
        data=column_data, context={"board": board}
    )
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def get_column(column_id):
    """Get a board column by ID or raise 404."""
    return get_object_or_404(BoardColumn, id=column_id)


def update_column(column_id, column_data):
    """Update a board column with partial data."""
    column = get_column(column_id)
    serializer = serializers.BoardColumnUpdateSerializer(
        column, data=column_data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def delete_column(column_id):
    """Delete a board column by ID."""
    column = get_column(column_id)
    column.delete()


def get_board_kanban(board_id):
    """Get kanban view for a board with columns and tasks."""
    board = get_board(board_id)
    return board
