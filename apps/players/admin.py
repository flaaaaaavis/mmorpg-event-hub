from django.contrib import admin
from .models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "guild", "created_at")
    list_filter = ("guild",)
    search_fields = ("user__username",)
    ordering = ("id",)
