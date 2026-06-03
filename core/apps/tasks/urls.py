from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.get_or_create_task, name="get-or-create-task"),
    path("<int:task_id>/", views.get_task_by_id, name="task-detail"),
    path("<int:task_id>/update/", views.partial_update_task, name="update-task"),
    path("<int:task_id>/delete/", views.delete_task, name="delete-task"),
    path(
        "<int:task_id>/comments/",
        views.get_or_create_task_comments,
        name="get-or-create-task-comment",
    ),
    path(
        "<int:task_id>/comments/<int:comment_id>/delete/",
        views.delete_task_comment,
        name="delete-task-comment",
    ),
]
