from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para o model User.
    Permite criar, atualizar, listar e detalhar users.
    """

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("id", "created_at")
