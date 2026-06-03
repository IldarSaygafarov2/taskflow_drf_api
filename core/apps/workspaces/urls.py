from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_create_workspaces, name="workspaces-list-create"),
    path("<int:workspace_id>/", views.get_workspace_detail, name="workspace-detail"),
    path(
        "<int:workspace_id>/update/",
        views.partial_update_workspace,
        name="workspace-partial-update",
    ),
    path("<int:workspace_id>/delete/", views.delete_workspace, name="workspace-delete"),
]
