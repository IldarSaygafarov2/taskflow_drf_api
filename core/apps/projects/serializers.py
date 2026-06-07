from rest_framework import serializers
from core.apps.workspaces.serializers import WorkspaceProjectSerializer
from core.apps.users.serializers import UserSerializer
from rest_framework.exceptions import ValidationError
from .models import Project


class ProjectListSerializer(serializers.ModelSerializer):
    workspace = WorkspaceProjectSerializer(many=False)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "status", "workspace"]


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["workspace", "name", "description", "start_date", "end_date"]

    def create(self, validated_data):
        request = self.context.get("request")

        start_date = validated_data.get("start_date")
        end_date = validated_data.get("end_date")

        if end_date < start_date:
            raise ValidationError(
                detail={"message": "end_date can't be less than start_date"}
            )

        return Project.objects.create(**validated_data, created_by=request.user)


class ProjectDetailSerializer(serializers.ModelSerializer):
    workspace = WorkspaceProjectSerializer(many=False)
    created_by = UserSerializer(many=False)

    class Meta:
        model = Project
        fields = [
            "id",
            "workspace",
            "name",
            "description",
            "start_date",
            "end_date",
            "status",
            "created_at",
            "updated_at",
            "created_by",
        ]


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "workspace",
            "name",
            "description",
            "start_date",
            "end_date",
            "status",
            "created_by",
        ]
