from rest_framework import serializers

from .models import Comment
from core.apps.users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer

    class Meta:
        model = Comment
        fields = ["id", "content", "author", "created_at"]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content"]
