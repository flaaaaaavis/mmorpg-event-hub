from rest_framework import viewsets

from apps.players.models import Player
from .serializers import PlayerSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o CRUD completo de Players.

    Operações suportadas:
    - list, retrieve, create, update, partial_update, destroy
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get_queryset(self):
        return Player.objects.all()
