from rest_framework import serializers

from core.apps.tasks.models import Task
from core.apps.tasks.serializers import TaskSerializer
from .models import Board, BoardColumn


class BoardProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "name", "created_at", "updated_at"]


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "name", "project", "created_at", "updated_at"]


class BoardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["name", "project"]


class BoardProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["name"]

    def create(self, validated_data):
        project = self.context.get("project")
        return Board.objects.create(**validated_data, project=project)


class BoardColumnCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardColumn
        fields = ["name", "position"]

    def create(self, validated_data):
        board = self.context.get("board")
        return BoardColumn.objects.create(**validated_data, board=board)


class BoardColumnUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardColumn
        fields = ["name", "position", "board"]


class BoardColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardColumn
        fields = ["id", "name", "position"]


class BoardKanbanColumnsSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField(method_name="get_column_tasks")

    class Meta:
        model = BoardColumn
        fields = ["id", "name", "position", "tasks"]

    def get_column_tasks(self, instance):
        tasks = Task.objects.filter(board_column=instance.id)
        tasks_serializer = TaskSerializer(tasks, many=True)
        return tasks_serializer.data


class BoardKanbanSerializer(serializers.ModelSerializer):
    columns = serializers.SerializerMethodField(method_name="get_columns")

    class Meta:
        model = Board
        fields = ["id", "name", "columns"]

    def get_columns(self, instance):
        columns = BoardColumn.objects.filter(board=instance)
        serializer = BoardKanbanColumnsSerializer(columns, many=True)
        return serializer.data
