from django.test import TestCase
from django.utils import timezone

from core.apps.comments.models import Comment
from core.apps.comments.serializers import CommentSerializer, CommentCreateSerializer
from core.apps.tasks.models import Task
from core.apps.projects.models import Project
from core.apps.workspaces.models import Workspace
from core.apps.boards.models import Board, BoardColumn
from core.apps.users.models import CustomUser


class CommentsAppTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="commenter",
            email="commenter@example.com",
            password="password123",
            first_name="Comment",
            last_name="User",
        )
        self.workspace = Workspace.objects.create(
            name="Workspace",
            description="Workspace description",
            owner=self.user,
            slug="workspace",
        )
        self.project = Project.objects.create(
            workspace=self.workspace,
            name="Project",
            description="Project description",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timezone.timedelta(days=30)).date(),
            created_by=self.user,
        )
        self.board = Board.objects.create(project=self.project, name="Board")
        self.board_column = BoardColumn.objects.create(
            board=self.board, name="Todo", position=1
        )
        self.task = Task.objects.create(
            project=self.project,
            board_column=self.board_column,
            title="Task",
            description="Task description",
            assignee=self.user,
            reporter=self.user,
            deadline=timezone.now() + timezone.timedelta(days=7),
            estimated_hours=5,
        )

    def test_comment_str_representation(self):
        comment = Comment.objects.create(
            task=self.task,
            author=self.user,
            content="A test comment",
        )

        self.assertIn(self.task.title, str(comment))
        self.assertIn(self.user.username, str(comment))

    def test_comment_serializer_includes_author_data(self):
        comment = Comment.objects.create(
            task=self.task,
            author=self.user,
            content="A second comment",
        )

        serializer = CommentSerializer(comment)

        self.assertEqual(serializer.data["content"], "A second comment")
        self.assertEqual(serializer.data["author"]["username"], self.user.username)
        self.assertIn("created_at", serializer.data)

    def test_comment_create_serializer_assigns_author_and_task(self):
        payload = {"content": "Serializer comment"}
        serializer = CommentCreateSerializer(
            data=payload,
            context={
                "request": type("R", (), {"user": self.user})(),
                "task": self.task,
            },
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

        comment = serializer.save()

        self.assertEqual(comment.content, "Serializer comment")
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.task, self.task)
