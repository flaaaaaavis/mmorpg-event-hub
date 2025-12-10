from typing import TYPE_CHECKING
from django.contrib import admin
from .models import Player

if TYPE_CHECKING:
    AdminBase = admin.ModelAdmin[Player]
else:
    AdminBase = admin.ModelAdmin

@admin.register(Player)
class PlayerAdmin(AdminBase):
    list_display = ("id", "user", "guild", "created_at")
    list_filter = ("guild",)
    search_fields = ("user__username",)
    ordering = ("id",)
