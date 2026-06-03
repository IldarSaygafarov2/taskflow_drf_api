from rest_framework import serializers

from .models import Task
from core.apps.comments.models import Comment


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title"]


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description"]


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "description"]
