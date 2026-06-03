from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.ProjectListCreateView.as_view(), name="projects-list-create"),
    path(
        "<int:id>/",
        views.ProjectRetrieveDestroyUpdateView.as_view(),
        name="project-retrive-update-delete",
    ),
]
