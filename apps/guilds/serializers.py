from typing import Any
from rest_framework import serializers
from apps.guilds.models import Guild


class GuildSerializer(serializers.ModelSerializer[Any]):
    class Meta:
        model = Guild
        fields = "__all__"
        read_only_fields = ("id", "created_at")
