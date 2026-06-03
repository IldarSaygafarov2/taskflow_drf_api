from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path("auth/login/", views.CustomTokenObtainPairView.as_view(), name="user-login"),
    path("auth/register/", views.UserRegistrationView.as_view(), name="user-register"),
    path(
        "auth/token/refresh/",
        views.CustomTokenRefreshView.as_view(),
        name="refresh-token",
    ),
]
