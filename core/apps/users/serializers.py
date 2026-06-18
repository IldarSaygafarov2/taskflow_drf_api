from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from core.apps.common.tasks import send_message_to_email

from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        send_message_to_email.delay(
            subject="Registration welcome message",
            message=f"Hello, {user.get_full_name()}. Welcome to our project",
            recipient=user.email,
        )
        return user


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    class Meta:
        model = RefreshToken
        fields = ["refresh_token"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email", "avatar"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "avatar"]
