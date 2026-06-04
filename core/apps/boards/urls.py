from django.urls import path

from . import views

urlpatterns = [
    path("<int:board_id>/", views.get_board, name="board-detail"),
    path("<int:board_id>/update/", views.update_board, name="board-update"),
    path("<int:board_id>/delete/", views.delete_board, name="board-delete"),
    path(
        "<int:board_id>/columns/",
        views.get_create_board_columns,
        name="board-columns",
    ),
    # columns
    path("columns/<int:column_id>/", views.get_column, name="column-detail"),
    path("columns/<int:column_id>/delete/", views.delete_column, name="column-delete"),
    path("columns/<int:column_id>/update/", views.update_column, name="column-update"),
]
