from typing import Any
from rest_framework import viewsets
from django.db.models import QuerySet

from apps.guilds.models import Guild
from .serializers import GuildSerializer


class GuildViewSet(viewsets.ModelViewSet[Any]):
    queryset = Guild.objects.all()
    serializer_class = GuildSerializer

    def get_queryset(self) -> QuerySet[Guild]:
        return Guild.objects.all()
