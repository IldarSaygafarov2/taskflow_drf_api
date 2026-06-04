from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.get_or_create_project, name="projects-list-create"),
    path("<int:project_id>/", views.get_project_detail, name="project-detail"),
    path("<int:project_id>/update/", views.update_project, name="project-update"),
    path("<int:project_id>/delete/", views.delete_project, name="delete-project"),
    path(
        "<int:project_id>/boards/",
        views.get_create_project_boards,
        name="project-boards",
    ),
]
