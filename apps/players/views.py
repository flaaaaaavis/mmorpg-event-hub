from typing import Any
from rest_framework import viewsets
from django.db.models import QuerySet

from apps.players.models import Player
from .serializers import PlayerSerializer


class PlayerViewSet(viewsets.ModelViewSet[Any]):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get_queryset(self) -> QuerySet[Player]:
        return Player.objects.all()