from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path("me/", views.get_or_update_user_info, name="get-or-update-user"),
    path("auth/login/", views.CustomTokenObtainPairView.as_view(), name="user-login"),
    path("auth/register/", views.UserRegistrationView.as_view(), name="user-register"),
    path("auth/logout/", views.LogoutView.as_view(), name="user-logout"),
    path(
        "auth/token/refresh/",
        views.CustomTokenRefreshView.as_view(),
        name="refresh-token",
    ),
]
