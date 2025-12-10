from rest_framework import serializers
from apps.guilds.models import Guild


class GuildSerializer(serializers.ModelSerializer):
    """
    Serializer para o model Guild.
    Permite criar, atualizar, listar e detalhar guilds.
    """

    class Meta:
        model = Guild
        fields = "__all__"
        read_only_fields = ("id", "created_at")
