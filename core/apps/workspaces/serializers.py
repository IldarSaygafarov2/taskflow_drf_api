from django.template.defaultfilters import slugify
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.apps.users.serializers import UserSerializer

from .models import Workspace, WorkspaceMember


class WorkspaceAbstractSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(method_name="get_owner")

    class Meta:
        abstract = True
        model = Workspace
        fields = ["id", "name", "slug", "owner", "created_at", "updated_at"]

    def get_owner(self, instance):
        owner_data = UserSerializer(instance.owner)
        return owner_data.data


class WorkspaceSerializer(WorkspaceAbstractSerializer):
    pass


class WorkspaceProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "name", "slug", "created_at", "updated_at"]


class WorkspaceDetailSerializer(WorkspaceAbstractSerializer):
    class Meta:
        model = Workspace
        fields = WorkspaceAbstractSerializer.Meta.fields + ["description"]


class WorkspaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["name", "description"]

    def create(self, validated_data):
        request = self.context.get("request")  # получаем контекст запроса
        slug = slugify(validated_data["name"])

        if Workspace.objects.filter(slug=slug).exists():
            raise ValidationError(
                {"message": "Workspace with this slug already exists"}
            )

        return Workspace.objects.create(**validated_data, owner=request.user, slug=slug)


class WorkspaceMemeberSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceMember
        fields = ["id", "user", "role", "created_at", "updated_at"]


class WorkspaceMemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceMember
        fields = ["user", "role"]

    def create(self, validated_data):
        workspace = self.context.get("workspace")
        return WorkspaceMember.objects.create(**validated_data, workspace=workspace)


class WorkspaceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["name", "description", "owner"]

    def update(self, instance, validated_data):
        slug = validated_data.get("name")
        if slug is not None:
            instance.slug = slugify(validated_data["name"])
        instance.save()
        return super().update(instance, validated_data)
