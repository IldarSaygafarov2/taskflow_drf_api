from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.apps.boards.models import Board, BoardColumn
from core.apps.projects.models import Project
from core.apps.tasks.models import Task
from core.apps.users.models import CustomUser
from core.apps.workspaces.models import Workspace


class BoardsAppTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="boarduser",
            email="board@example.com",
            password="password123",
            first_name="Board",
            last_name="User",
        )

        self.workspace = Workspace.objects.create(
            name="Workspace Test",
            description="Workspace desc",
            owner=self.user,
            slug="workspace-test",
        )

        self.project = Project.objects.create(
            workspace=self.workspace,
            name="Project Test",
            description="Project desc",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=30)).date(),
            created_by=self.user,
        )

        self.board = Board.objects.create(project=self.project, name="Board 1")
        self.column = BoardColumn.objects.create(
            board=self.board, name="Todo", position=1
        )

        self.detail_url = reverse("boards:board-detail", args=[self.board.id])
        self.kanban_url = reverse("boards:kanban-table", args=[self.board.id])
        self.columns_url = reverse("boards:board-columns", args=[self.board.id])

    def _authenticate(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        return refresh

    def test_get_board_detail_patch_delete(self):
        self._authenticate()

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Board 1")

        patch_payload = {"name": "Board Updated"}
        response = self.client.patch(self.detail_url, patch_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Board Updated")

        delete_response = self.client.delete(self.detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertFalse(Board.objects.filter(id=self.board.id).exists())

    def test_create_and_list_board_columns(self):
        self._authenticate()
        # list existing
        response = self.client.get(self.columns_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        payload = {"name": "In Progress", "position": 2}
        response = self.client.post(self.columns_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "In Progress")
        self.assertTrue(
            BoardColumn.objects.filter(board=self.board, name="In Progress").exists()
        )

    def test_column_get_patch_delete(self):
        self._authenticate()
        column_detail = reverse("boards:column-detail", args=[self.column.id])

        response = self.client.get(column_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Todo")

        response = self.client.patch(column_detail, {"name": "Backlog"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.column.refresh_from_db()
        self.assertEqual(self.column.name, "Backlog")

        response = self.client.delete(column_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(BoardColumn.objects.filter(id=self.column.id).exists())

    def test_kanban_returns_columns_and_tasks(self):
        # create another column and a task in it
        col2 = BoardColumn.objects.create(board=self.board, name="Done", position=2)
        task = Task.objects.create(
            project=self.project,
            board_column=col2,
            title="Task K",
            description="Task K desc",
            assignee=self.user,
            reporter=self.user,
            deadline=timezone.now() + timedelta(days=3),
            estimated_hours=2,
        )

        response = self.client.get(self.kanban_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # columns should be present
        self.assertIn("columns", response.data)
        columns = response.data["columns"]
        self.assertTrue(any(c["name"] == "Todo" for c in columns))
        self.assertTrue(any(c["name"] == "Done" for c in columns))
        # check tasks included for Done column
        done_col = next((c for c in columns if c["name"] == "Done"), None)
        self.assertIsNotNone(done_col)
        self.assertTrue(any(t["title"] == "Task K" for t in done_col.get("tasks", [])))
