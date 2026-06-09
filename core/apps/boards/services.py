from core.apps.tasks.models import TaskStatus

from .models import BoardColumn


def create_default_columns(board):
    task_status_choices = [choice[0] for choice in TaskStatus.choices]

    for idx, choice in enumerate(task_status_choices, start=1):
        BoardColumn.objects.create(board=board, name=choice.upper(), position=idx)

    print(f"DEFAULT COLUMNS CREATED")
