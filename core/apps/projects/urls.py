from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.get_or_create_project, name="projects-list-create"),
    path("<int:project_id>/", views.get_delete_update_project, name="project-detail"),
    path(
        "<int:project_id>/boards/",
        views.get_create_project_boards,
        name="project-boards",
    ),
]
