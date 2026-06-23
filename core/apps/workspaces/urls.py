from django.urls import path

from . import views

app_name = "workspaces"

urlpatterns = [
    path("", views.get_create_workspaces, name="workspaces-list-create"),
    path(
        "<int:workspace_id>/",
        views.workspace_detail_delete_patch,
        name="workspace-detail",
    ),
    path(
        "<int:workspace_id>/members/",
        views.get_or_create_workspace_members,
        name="workspace-members",
    ),
]
