from rest_framework.response import Response

from core.project.settings import BASE_DIR

from .serializers import UserSerializer, UserUpdateSerializer
from pathlib import Path


def get_user_info(request):
    user_serializer = UserSerializer(request.user)
    return Response(data=user_serializer.data)


def update_user_data(request):
    data = request.data
    user_avatar = data.get("avatar")
    if user_avatar is not None:
        data["avatar"].name = f"{request.user.username}.jpg"

    user_serializer = UserUpdateSerializer(
        request.user, data=request.data, partial=True
    )
    user_serializer.is_valid(raise_exception=True)
    user_serializer.save()
    updated_user_data = get_user_info(request)
    return Response(data=updated_user_data.data)
