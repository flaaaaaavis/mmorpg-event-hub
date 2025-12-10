from rest_framework import serializers
from apps.players.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    """
    Serializer para o model Player.
    Permite criar, atualizar, listar e detalhar players.
    """

    class Meta:
        model = Player
        fields = "__all__"
        read_only_fields = ("id", "created_at")
