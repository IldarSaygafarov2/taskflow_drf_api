from django.urls import path

from . import views

app_name = "workspaces"

urlpatterns = [
    path("", views.get_create_workspaces, name="workspaces-list-create"),
    path("<int:workspace_id>/", views.get_workspace_detail, name="workspace-detail"),
    path(
        "<int:workspace_id>/update/",
        views.partial_update_workspace,
        name="workspace-partial-update",
    ),
    path("<int:workspace_id>/delete/", views.delete_workspace, name="workspace-delete"),
    path(
        "<int:workspace_id>/members/",
        views.get_or_create_workspace_members,
        name="workspace-members",
    ),
]
