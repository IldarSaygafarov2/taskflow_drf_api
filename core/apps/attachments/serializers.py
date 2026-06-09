import os

from rest_framework import serializers

from core.apps.users.serializers import UserSerializer
from core.project.settings import SUPPORTED_FILE_SUFFIXES
from rest_framework.exceptions import ValidationError

from .models import Attachment


class AttachmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ["file"]

    def create(self, validated_data):
        request = self.context.get("request")
        task = self.context.get("task")

        file = validated_data.get("file")

        _, extension = os.path.splitext(file.name)

        if extension not in SUPPORTED_FILE_SUFFIXES:
            raise ValidationError({"message": "unsupported extension of file"})

        return Attachment.objects.create(
            **validated_data, uploaded_by=request.user, task=task
        )


class AttachmentReadSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer()

    class Meta:
        model = Attachment
        fields = ["id", "file", "uploaded_by"]
