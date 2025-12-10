from typing import TYPE_CHECKING
from django.contrib import admin
from .models import Event

if TYPE_CHECKING:
    AdminBase = admin.ModelAdmin[Event]
else:
    AdminBase = admin.ModelAdmin

@admin.register(Event)
class EventAdmin(AdminBase):
    list_display = ("id", "type", "player", "guild", "created_at")
    list_filter = ("type", "guild")
    search_fields = ("type", "player__user__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
