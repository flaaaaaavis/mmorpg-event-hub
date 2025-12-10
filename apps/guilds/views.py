from rest_framework import viewsets

from apps.guilds.models import Guild
from .serializers import GuildSerializer


class GuildViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o CRUD completo de Guilds.
    
    Operações suportadas:
    - list, retrieve, create, update, partial_update, destroy
    """
    queryset = Guild.objects.all()
    serializer_class = GuildSerializer

    def get_queryset(self):
        return Guild.objects.all()
