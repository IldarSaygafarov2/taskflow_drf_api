from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Task
from core.apps.comments.models import Comment


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "priority", "status", "assignee"]


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
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
        ]

    def create(self, validated_data):
        estimated_hours = validated_data.get("estimated_hours")

        if estimated_hours <= 0:
            raise ValidationError({"message": "invalid data"})

        return super().create(validated_data)
