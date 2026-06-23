from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.apps.users.models import CustomUser
from core.apps.users.serializers import UserRegistrationSerializer


class UsersAppTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
        )
        self.user_url = reverse("get-or-update-user")
        self.register_url = reverse("user-register")
        self.logout_url = reverse("user-logout")

    def _authenticate(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        return refresh

    def test_get_user_info(self):
        self._authenticate()

        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["email"], self.user.email)

    def test_patch_user_info(self):
        self._authenticate()

        payload = {
            "first_name": "Updated",
            "last_name": "Name",
            "email": "updated@example.com",
        }
        response = self.client.patch(self.user_url, payload, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.email, "updated@example.com")
        self.assertEqual(response.data["email"], "updated@example.com")

    def test_registration_serializer_password_mismatch(self):
        payload = {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@example.com",
            "password": "password1",
            "password2": "password2",
        }
        serializer = UserRegistrationSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    @patch("core.apps.users.serializers.send_message_to_email.delay")
    @patch("core.apps.users.views.async_to_sync")
    @patch("core.apps.users.views.get_channel_layer")
    def test_register_creates_user(
        self, mock_get_channel_layer, mock_async_to_sync, mock_send_message
    ):
        mock_channel_layer = mock_get_channel_layer.return_value
        mock_channel_layer.group_send.return_value = None

        payload = {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@example.com",
            "password": "password123",
            "password2": "password123",
        }
        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username="newuser").exists())

        user = CustomUser.objects.get(username="newuser")
        self.assertTrue(user.check_password("password123"))
        self.assertEqual(response.data["username"], "newuser")
        mock_send_message.assert_called_once()
        mock_get_channel_layer.assert_called_once()
        mock_async_to_sync.assert_called_once()

    def test_logout_blacklists_refresh_token(self):
        refresh = self._authenticate()

        response = self.client.post(
            self.logout_url, {"refresh_token": str(refresh)}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
