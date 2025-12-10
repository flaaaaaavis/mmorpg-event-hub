from django.contrib import admin
from .models import Guild

@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "score", "created_at")
    search_fields = ("name",)
    ordering = ("id",)
