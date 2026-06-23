from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.apps.users.models import CustomUser
from core.apps.workspaces.models import Workspace, WorkspaceMember


class WorkspaceAppTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = CustomUser.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
            first_name="Owner",
            last_name="User",
        )
        self.other_user = CustomUser.objects.create_user(
            username="member",
            email="member@example.com",
            password="password123",
            first_name="Member",
            last_name="User",
        )
        self.list_create_url = reverse("workspaces:workspaces-list-create")

    def _authenticate(self):
        refresh = RefreshToken.for_user(self.owner)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        return refresh

    def test_get_workspaces_list(self):
        self._authenticate()
        workspace = Workspace.objects.create(
            name="Workspace 1",
            description="Test workspace",
            owner=self.owner,
            slug="workspace-1",
        )

        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], workspace.id)
        self.assertEqual(response.data[0]["name"], "Workspace 1")

    @patch("core.apps.workspaces.views.get_channel_layer")
    @patch("core.apps.workspaces.views.async_to_sync")
    def test_create_workspace(self, mock_async_to_sync, mock_get_channel_layer):
        self._authenticate()
        mock_channel_layer = mock_get_channel_layer.return_value
        mock_channel_layer.group_send.return_value = None

        payload = {
            "name": "New Workspace",
            "description": "Workspace description",
        }
        response = self.client.post(self.list_create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Workspace.objects.filter(name="New Workspace").exists())
        workspace = Workspace.objects.get(name="New Workspace")
        self.assertEqual(workspace.slug, "new-workspace")
        self.assertEqual(response.data["slug"], "new-workspace")
        mock_get_channel_layer.assert_called_once()
        mock_async_to_sync.assert_called_once()

    def test_workspace_detail_get_patch_delete(self):
        self._authenticate()
        workspace = Workspace.objects.create(
            name="Workspace Example",
            description="Initial description",
            owner=self.owner,
            slug="workspace-example",
        )
        detail_url = reverse("workspaces:workspace-detail", args=[workspace.id])

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Workspace Example")

        patch_payload = {"name": "Updated Workspace", "description": "Updated"}
        response = self.client.patch(detail_url, patch_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        workspace.refresh_from_db()
        self.assertEqual(workspace.name, "Updated Workspace")
        self.assertEqual(workspace.slug, "updated-workspace")
        self.assertEqual(response.data["slug"], "updated-workspace")

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertFalse(Workspace.objects.filter(id=workspace.id).exists())

    def test_get_and_add_workspace_member(self):
        self._authenticate()
        workspace = Workspace.objects.create(
            name="Member Workspace",
            description="Workspace with members",
            owner=self.owner,
            slug="member-workspace",
        )
        members_url = reverse("workspaces:workspace-members", args=[workspace.id])

        response = self.client.get(members_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

        payload = {"user": self.other_user.id, "role": "member"}
        response = self.client.post(members_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], self.other_user.id)
        self.assertEqual(response.data["role"], "member")
        self.assertTrue(
            WorkspaceMember.objects.filter(
                workspace=workspace, user=self.other_user, role="member"
            ).exists()
        )
