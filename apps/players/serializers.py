from typing import Any
from rest_framework import serializers
from apps.players.models import Player


class PlayerSerializer(serializers.ModelSerializer[Any]):
    class Meta:
        model = Player
        fields = "__all__"
        read_only_fields = ("id", "created_at")
