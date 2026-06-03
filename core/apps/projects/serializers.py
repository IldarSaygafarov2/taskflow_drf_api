from rest_framework import serializers

from . import models


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ["id", "name", "description"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ["id", "name", "description", "created_at", "updated_at"]
