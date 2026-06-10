from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .services import get_user_info, update_user_data


@swagger_auto_schema(
    method="get",
    operation_id="get_user_info",
    responses={200: serializers.UserSerializer},
)
@swagger_auto_schema(
    method="patch",
    operation_id="update_user_info",
    request_body=serializers.UserUpdateSerializer,
    responses={200: serializers.UserSerializer},
)
@api_view(["GET", "PATCH"])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def get_or_update_user_info(request):
    if request.method == "GET":
        return get_user_info(request)

    # updating user data
    return update_user_data(request)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = serializers.UserRegistrationSerializer

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(tags=["Auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(tags=["Auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(tags=["Auth"], request_body=serializers.LogoutSerializer)
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
