from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from core.apps.attachments.serializers import (
    AttachmentCreateSerializer,
    AttachmentReadSerializer,
)
from core.apps.attachments.models import Attachment
from core.apps.users.models import CustomUser
from core.apps.workspaces.models import Workspace
from core.apps.projects.models import Project
from core.apps.boards.models import Board, BoardColumn
from core.apps.tasks.models import Task


class AttachmentsAppTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="attachuser",
            email="attach@example.com",
            password="password123",
            first_name="Attach",
            last_name="User",
        )

        self.workspace = Workspace.objects.create(
            name="Workspace A",
            description="Workspace A",
            owner=self.user,
            slug="workspace-a",
        )

        self.project = Project.objects.create(
            workspace=self.workspace,
            name="Project A",
            description="Project A",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timezone.timedelta(days=30)).date(),
            created_by=self.user,
        )

        self.board = Board.objects.create(project=self.project, name="Board A")
        self.column = BoardColumn.objects.create(
            board=self.board, name="Todo", position=1
        )

        self.task = Task.objects.create(
            project=self.project,
            board_column=self.column,
            title="Task A",
            description="Task A",
            assignee=self.user,
            reporter=self.user,
            deadline=timezone.now() + timezone.timedelta(days=7),
            estimated_hours=3,
        )

    def test_attachment_create_serializer_valid_extension(self):
        # create a small in-memory file with supported extension
        test_file = SimpleUploadedFile(
            "test.pdf", b"filecontent", content_type="application/pdf"
        )

        serializer = AttachmentCreateSerializer(
            data={"file": test_file},
            context={
                "request": type("R", (), {"user": self.user})(),
                "task": self.task,
            },
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        attachment = serializer.save()

        self.assertIsInstance(attachment, Attachment)
        self.assertEqual(attachment.uploaded_by, self.user)
        self.assertEqual(attachment.task, self.task)

    def test_attachment_create_serializer_invalid_extension(self):
        from rest_framework.exceptions import ValidationError

        bad_file = SimpleUploadedFile(
            "malware.exe", b"binary", content_type="application/octet-stream"
        )

        serializer = AttachmentCreateSerializer(
            data={"file": bad_file},
            context={
                "request": type("R", (), {"user": self.user})(),
                "task": self.task,
            },
        )

        # validation happens on save in create(), so is_valid() may be True
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidationError) as cm:
            serializer.save()

        self.assertIn("message", cm.exception.detail)

    def test_attachment_read_serializer_includes_uploaded_by(self):
        attachment = Attachment.objects.create(
            file=SimpleUploadedFile("a.pdf", b"x"),
            uploaded_by=self.user,
            task=self.task,
        )

        serializer = AttachmentReadSerializer(attachment)
        self.assertIn("uploaded_by", serializer.data)
        self.assertEqual(serializer.data["uploaded_by"]["username"], self.user.username)
