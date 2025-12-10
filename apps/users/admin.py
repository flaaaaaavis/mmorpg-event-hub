from typing import TYPE_CHECKING
from django.contrib import admin
from .models import User

if TYPE_CHECKING:
    AdminBase = admin.ModelAdmin[User]
else:
    AdminBase = admin.ModelAdmin

@admin.register(User)
class UserAdmin(AdminBase):
    list_display = ("id", "username", "created_at")
    search_fields = ("username",)
    ordering = ("id",)
