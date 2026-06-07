from rest_framework import serializers

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
