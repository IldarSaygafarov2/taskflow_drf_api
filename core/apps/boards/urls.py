from django.urls import path

from . import views

app_name = "boards"

urlpatterns = [
    path("<int:board_id>/", views.get_update_delete_board, name="board-detail"),
    path(
        "<int:board_id>/columns/",
        views.get_create_board_columns,
        name="board-columns",
    ),
    # columns
    path(
        "columns/<int:column_id>/", views.get_update_delete_column, name="column-detail"
    ),
]
