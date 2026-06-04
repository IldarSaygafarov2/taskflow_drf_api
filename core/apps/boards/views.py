from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view


@swagger_auto_schema(method="get", operation_id="get_board_by_id")
@api_view(["GET"])
def get_board(request, board_id):
    pass


@swagger_auto_schema(method="patch", operation_id="update_board")
@api_view(["PATCH"])
def update_board(request, board_id):
    pass


@swagger_auto_schema(method="delete", operation_id="delete_board")
@api_view(["DELETE"])
def delete_board(request, board_id):
    pass


@swagger_auto_schema(method="post", operation_id="create_board_column")
@swagger_auto_schema(method="get", operation_id="get_board_columns")
@api_view(["GET", "POST"])
def get_create_board_columns(request, board_id):
    pass


@swagger_auto_schema(method="get", operation_id="get_column")
@api_view(["GET"])
def get_column(request, column_id):
    pass


@swagger_auto_schema(method="patch", operation_id="update_column")
@api_view(["PATCH"])
def update_column(request, column_id):
    pass


@swagger_auto_schema(method="delete", operation_id="delete_column")
@api_view(["DELETE"])
def delete_column(request, column_id):
    pass


# @swagger_auto_schema(method="post", operation_id="reorder_columns")
# @api_view(["POST"])
# def reorder_columns(request, board_id):
#     pass


# @swagger_auto_schema(method="post", operation_id="reorder_columns")
# @api_view(["POST"])
# def reorder_columns(request, board_id):
#     pass
