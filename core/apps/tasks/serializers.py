from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.apps.comments.models import Comment
from core.apps.users.serializers import UserSerializer
from core.apps.projects.serializers import ProjectListSerializer

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    assignee = UserSerializer()

    class Meta:
        model = Task
        fields = ["id", "title", "priority", "status", "assignee"]


class TaskDetailSerializer(serializers.ModelSerializer):
    assignee = UserSerializer()
    reporter = UserSerializer()
    project = ProjectListSerializer()

    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "title",
            "description",
            "estimated_hours",
            "priority",
            "status",
            "assignee",
            "reporter",
            "created_at",
            "updated_at",
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "project",
            "board_column",
            "title",
            "description",
            "assignee",
            "reporter",
            "deadline",
            "estimated_hours",
            "spent_hours",
        ]

    def create(self, validated_data):
        estimated_hours = validated_data.get("estimated_hours")

        if estimated_hours <= 0:
            raise ValidationError({"message": "invalid data"})

        return super().create(validated_data)


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "project",
            "title",
            "description",
            "assignee",
            "reporter",
            "deadline",
            "estimated_hours",
            "status",
            "priority",
        ]
