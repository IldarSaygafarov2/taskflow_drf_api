from django.contrib import admin
from unfold import admin as unfold_admin

from .models import Board, BoardColumn


class BoardColumnInline(unfold_admin.TabularInline):
    model = BoardColumn
    extra = 1


@admin.register(Board)
class BoardAdmin(unfold_admin.ModelAdmin):
    inlines = [BoardColumnInline]
