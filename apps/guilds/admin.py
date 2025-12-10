from typing import TYPE_CHECKING
from django.contrib import admin
from .models import Guild

if TYPE_CHECKING:
    AdminBase = admin.ModelAdmin[Guild]
else:
    AdminBase = admin.ModelAdmin

@admin.register(Guild)
class GuildAdmin(AdminBase):
    list_display = ("id", "name", "score", "created_at")
    search_fields = ("name",)
    ordering = ("id",)
