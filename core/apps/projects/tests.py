from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.apps.users.models import CustomUser
from core.apps.workspaces.models import Workspace
from core.apps.projects.models import Project, ProjectStatus
from core.apps.boards.models import Board


class ProjectsAppTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = CustomUser.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
            first_name="Owner",
            last_name="User",
        )
        self.workspace = Workspace.objects.create(
            name="Workspace A",
            description="Workspace A description",
            owner=self.owner,
            slug="workspace-a",
        )
        self.list_create_url = reverse("projects:projects-list-create")

    def _authenticate(self):
        refresh = RefreshToken.for_user(self.owner)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        return refresh

    def test_get_projects_list(self):
        self._authenticate()
        project = Project.objects.create(
            workspace=self.workspace,
            name="Project A",
            description="Test project",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=30)).date(),
            created_by=self.owner,
        )

        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], project.id)
        self.assertEqual(response.data[0]["name"], "Project A")

    def test_get_projects_list_filter_status(self):
        self._authenticate()
        Project.objects.create(
            workspace=self.workspace,
            name="Project A",
            description="Test project",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=30)).date(),
            created_by=self.owner,
            status=ProjectStatus.ACTIVE,
        )
        Project.objects.create(
            workspace=self.workspace,
            name="Project B",
            description="Test project",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=30)).date(),
            created_by=self.owner,
            status=ProjectStatus.ARCHIVED,
        )

        response = self.client.get(
            self.list_create_url, {"status": ProjectStatus.ARCHIVED}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Project B")

    def test_create_project(self):
        self._authenticate()

        payload = {
            "workspace": self.workspace.id,
            "name": "New Project",
            "description": "Project description",
            "start_date": timezone.now().date().isoformat(),
            "end_date": (timezone.now() + timedelta(days=30)).date().isoformat(),
        }
        response = self.client.post(self.list_create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "New Project")
        self.assertEqual(response.data["workspace"]["id"], self.workspace.id)
        self.assertTrue(Project.objects.filter(name="New Project").exists())

    def test_create_project_end_date_before_start_date(self):
        self._authenticate()

        payload = {
            "workspace": self.workspace.id,
            "name": "Invalid Project",
            "description": "Project description",
            "start_date": timezone.now().date().isoformat(),
            "end_date": (timezone.now() - timedelta(days=1)).date().isoformat(),
        }
        response = self.client.post(self.list_create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)

    def test_project_detail_update_and_delete(self):
        self._authenticate()
        project = Project.objects.create(
            workspace=self.workspace,
            name="Project A",
            description="Test project",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=30)).date(),
            created_by=self.owner,
        )
        detail_url = reverse("projects:project-detail", args=[project.id])

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Project A")

        patch_payload = {"name": "Updated Project", "status": ProjectStatus.COMPLETED}
        response = self.client.patch(detail_url, patch_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        self.assertEqual(project.name, "Updated Project")
        self.assertEqual(project.status, ProjectStatus.COMPLETED)

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertFalse(Project.objects.filter(id=project.id).exists())

    def test_create_project_board(self):
        self._authenticate()
        project = Project.objects.create(
            workspace=self.workspace,
            name="Project Board",
            description="Test project",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=30)).date(),
            created_by=self.owner,
        )
        board_url = reverse("projects:project-boards", args=[project.id])

        payload = {"name": "Project Board 1"}
        response = self.client.post(board_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Project Board 1")
        self.assertTrue(
            Board.objects.filter(project=project, name="Project Board 1").exists()
        )
