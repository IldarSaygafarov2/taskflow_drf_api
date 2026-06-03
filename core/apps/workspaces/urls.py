from django.urls import path

from . import views

urlpatterns = [
    path("", views.WorkspacesListView.as_view(), name="workspaces-list"),
    path(
        "<slug:slug>/", views.WorkSpacesDetailView.as_view(), name="workspaces-detail"
    ),
]
