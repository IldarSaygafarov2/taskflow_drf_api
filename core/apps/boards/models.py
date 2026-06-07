from django.db import models

from core.apps.common.models import BaseModel


class Board(BaseModel):
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, verbose_name="Project"
    )
    name = models.CharField(verbose_name="name", max_length=255)

    def __str__(self):
        return f"{self.project.name} - {self.name}"

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"


class BoardColumn(BaseModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name="Board")
    name = models.CharField(verbose_name="name", max_length=255)
    position = models.PositiveIntegerField(verbose_name="position")

    def __str__(self):
        return f"{self.board.name} - {self.position}"

    class Meta:
        verbose_name = "BoardColumn"
        verbose_name_plural = "BoardColumns"
