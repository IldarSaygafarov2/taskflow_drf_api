from rest_framework import serializers

from .models import Workspace, WorkspaceMember


class WorkspaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "name"]


class WorkspaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["name"]


class WorkspaceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "name", "description"]
