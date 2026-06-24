from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.apps.attachments.serializers import AttachmentReadSerializer
from core.apps.users.models import CustomUser
from core.apps.workspaces.models import Workspace
from core.apps.projects.models import Project
from core.apps.boards.models import Board, BoardColumn
from core.apps.tasks.models import Task
from core.apps.tasks.models import TaskPriority, TaskStatus
from core.apps.tasks.serializers import TaskCreateSerializer
from core.apps.tasks.serializers import TaskSerializer
from core.apps.tasks.serializers import TaskDetailSerializer
from core.apps.comments.models import Comment


class TasksAppTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = CustomUser.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
            first_name="Owner",
            last_name="User",
        )
        self.assignee = CustomUser.objects.create_user(
            username="assignee",
            email="assignee@example.com",
            password="password123",
            first_name="Assignee",
            last_name="User",
        )
        self.reporter = CustomUser.objects.create_user(
            username="reporter",
            email="reporter@example.com",
            password="password123",
            first_name="Reporter",
            last_name="User",
        )
        self.workspace = Workspace.objects.create(
            name="Workspace A",
            description="Workspace A description",
            owner=self.owner,
            slug="workspace-a",
        )
        self.project = Project.objects.create(
            workspace=self.workspace,
            name="Project A",
            description="Project description",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=30)).date(),
            created_by=self.owner,
        )
        self.board = Board.objects.create(
            project=self.project,
            name="Board A",
        )
        self.board_column = BoardColumn.objects.create(
            board=self.board,
            name="Todo",
            position=1,
        )
        self.list_create_url = reverse("tasks:get-or-create-task")

    def _authenticate(self):
        refresh = RefreshToken.for_user(self.owner)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        return refresh

    @patch("core.apps.tasks.services.schedule_email")
    def test_get_tasks_list(self, mock_send):
        self._authenticate()
        task = Task.objects.create(
            project=self.project,
            board_column=self.board_column,
            title="Task 1",
            description="Description",
            assignee=self.assignee,
            reporter=self.reporter,
            deadline=timezone.now() + timedelta(days=5),
            estimated_hours=3.5,
            priority=TaskPriority.HIGH,
            status=TaskStatus.IN_PROGRESS,
        )

        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], task.id)
        self.assertEqual(response.data[0]["title"], "Task 1")

    @patch("core.apps.tasks.services.schedule_email")
    def test_filter_tasks_by_status_and_priority(self, mock_send):
        self._authenticate()
        Task.objects.create(
            project=self.project,
            board_column=self.board_column,
            title="Task Low",
            description="Description",
            assignee=self.assignee,
            reporter=self.reporter,
            deadline=timezone.now() + timedelta(days=5),
            estimated_hours=2,
            priority=TaskPriority.LOW,
            status=TaskStatus.TODO,
        )
        Task.objects.create(
            project=self.project,
            board_column=self.board_column,
            title="Task High",
            description="Description",
            assignee=self.assignee,
            reporter=self.reporter,
            deadline=timezone.now() + timedelta(days=6),
            estimated_hours=2,
            priority=TaskPriority.HIGH,
            status=TaskStatus.IN_PROGRESS,
        )

        response = self.client.get(
            self.list_create_url,
            {"status": TaskStatus.IN_PROGRESS, "priority": TaskPriority.HIGH},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Task High")

    @patch("core.apps.tasks.services.schedule_email")
    def test_create_task(self, mock_send_message):
        self._authenticate()

        payload = {
            "project": self.project.id,
            "board_column": self.board_column.id,
            "title": "New Task",
            "description": "Task description",
            "assignee": self.assignee.id,
            "reporter": self.reporter.id,
            "deadline": (timezone.now() + timedelta(days=7)).isoformat(),
            "estimated_hours": "5.00",
            "spent_hours": "0.00",
        }
        response = self.client.post(self.list_create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "New Task")
        self.assertEqual(response.data["status"], TaskStatus.TODO)
        self.assertEqual(response.data["priority"], TaskPriority.LOW)
        self.assertEqual(response.data["assignee"]["email"], self.assignee.email)
        self.assertTrue(Task.objects.filter(title="New Task").exists())
        self.assertEqual(mock_send_message.call_count, 2)

    @patch("core.apps.tasks.services.schedule_email")
    def test_create_task_invalid_estimated_hours(self, mock_send_message):
        self._authenticate()
        payload = {
            "project": self.project.id,
            "board_column": self.board_column.id,
            "title": "Bad Task",
            "description": "Task description",
            "assignee": self.assignee.id,
            "reporter": self.reporter.id,
            "deadline": (timezone.now() + timedelta(days=7)).isoformat(),
            "estimated_hours": "0.00",
            "spent_hours": "0.00",
        }

        response = self.client.post(self.list_create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)

    @patch("core.apps.tasks.services.schedule_email")
    def test_task_detail_update_and_delete(self, mock_send_message):
        self._authenticate()
        task = Task.objects.create(
            project=self.project,
            board_column=self.board_column,
            title="Task Detail",
            description="Description",
            assignee=self.assignee,
            reporter=self.reporter,
            deadline=timezone.now() + timedelta(days=5),
            estimated_hours=1,
            priority=TaskPriority.LOW,
            status=TaskStatus.TODO,
        )
        detail_url = reverse("tasks:task-detail", args=[task.id])

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Task Detail")

        patch_payload = {"title": "Task Updated", "status": TaskStatus.REVIEW}
        response = self.client.patch(detail_url, patch_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, "Task Updated")
        self.assertEqual(task.status, TaskStatus.REVIEW)

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    @patch("core.apps.tasks.services.schedule_email")
    def test_task_comments_create_and_delete(self, mock_send_message):
        self._authenticate()
        task = Task.objects.create(
            project=self.project,
            board_column=self.board_column,
            title="Task Comment",
            description="Description",
            assignee=self.assignee,
            reporter=self.reporter,
            deadline=timezone.now() + timedelta(days=5),
            estimated_hours=4,
        )
        comments_url = reverse("tasks:get-or-create-task-comment", args=[task.id])

        payload = {"content": "This is a comment"}
        response = self.client.post(comments_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "This is a comment")
        self.assertTrue(
            Comment.objects.filter(task=task, content="This is a comment").exists()
        )

        comment = Comment.objects.get(task=task, content="This is a comment")
        delete_url = reverse("tasks:delete-task-comment", args=[task.id, comment.id])
        delete_response = self.client.delete(delete_url)
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())
