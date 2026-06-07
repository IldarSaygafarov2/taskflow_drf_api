from django.db import models

from core.apps.common.models import BaseModel


class TaskStatus(models.TextChoices):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"


class TaskPriority(models.TextChoices):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Task(BaseModel):
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, verbose_name="Project"
    )
    board_column = models.ForeignKey(
        "boards.BoardColumn", on_delete=models.CASCADE, verbose_name="Board column"
    )
    title = models.CharField(verbose_name="Title", max_length=150)
    description = models.TextField(verbose_name="Description")
    status = models.CharField(
        verbose_name="Status",
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
    )
    priority = models.CharField(
        verbose_name="Priority",
        choices=TaskPriority.choices,
        default=TaskPriority.LOW,
    )
    assignee = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name="Assignee",
        related_name="assigned_tasks",
    )
    reporter = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name="Reporter",
        related_name="reported_tasks",
    )
    deadline = models.DateTimeField(verbose_name="Task deadline")
    estimated_hours = models.DecimalField(
        verbose_name="Estimated hours", max_digits=5, decimal_places=2
    )
    spent_hours = models.DecimalField(
        verbose_name="Spent hours",
        max_digits=5,
        decimal_places=2,
        default=0,
    )
    is_completed = models.BooleanField(verbose_name="Is completed", default=False)
    is_deleted = models.BooleanField(verbose_name="Is deleted", default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
