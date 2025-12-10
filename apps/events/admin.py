from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "player", "guild", "created_at")
    list_filter = ("type", "guild")
    search_fields = ("type", "player__user__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
