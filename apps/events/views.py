from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q, Count, Max, Min
from django.utils import timezone
from datetime import timedelta

from apps.events.models import Event, EventType
from apps.events.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o CRUD completo de Events.

    Operações suportadas:
    - list, retrieve, create, update, partial_update, destroy
    - Ações customizadas: statistics (player, guild, global)
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Event.objects.all()
        
        # Filtro por tipo de evento
        event_type = self.request.query_params.get('type')
        if event_type:
            queryset = queryset.filter(type=event_type)
        
        # Filtro por player
        player_id = self.request.query_params.get('player_id')
        if player_id:
            queryset = queryset.filter(player_id=player_id)
        
        # Filtro por guild
        guild_id = self.request.query_params.get('guild_id')
        if guild_id:
            queryset = queryset.filter(guild_id=guild_id)
        
        # Filtro por intervalo de datas
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        return queryset

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Retorna estatísticas globais do sistema."""
        total_events = Event.objects.count()
        events_by_type = Event.objects.values('type').annotate(count=Count('type'))
        top_players = Event.objects.filter(player__isnull=False).values('player__user__username').annotate(count=Count('id')).order_by('-count')[:10]
        top_guilds = Event.objects.filter(guild__isnull=False).values('guild__name').annotate(count=Count('id')).order_by('-count')[:10]
        
        return Response({
            'total_events': total_events,
            'events_by_type': list(events_by_type),
            'top_players': list(top_players),
            'top_guilds': list(top_guilds),
        })

    @action(detail=False, methods=['get'])
    def player_stats(self, request):
        """Retorna estatísticas de atividade de um player."""
        player_id = request.query_params.get('player_id')
        if not player_id:
            return Response(
                {'error': 'player_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        events = Event.objects.filter(player_id=player_id)
        if not events.exists():
            return Response(
                {'error': 'Player não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        total_events = events.count()
        event_types = events.values('type').annotate(count=Count('type'))
        last_activity = events.aggregate(Max('created_at'))['created_at__max']
        guilds = events.filter(guild__isnull=False).values('guild__id', 'guild__name').distinct()
        
        return Response({
            'player_id': str(player_id),
            'total_events': total_events,
            'event_types': list(event_types),
            'last_activity': last_activity,
            'guilds_related': list(guilds),
        })

    @action(detail=False, methods=['get'])
    def guild_stats(self, request):
        """Retorna estatísticas de atividade de uma guild."""
        guild_id = request.query_params.get('guild_id')
        if not guild_id:
            return Response(
                {'error': 'guild_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        events = Event.objects.filter(guild_id=guild_id)
        if not events.exists():
            return Response(
                {'error': 'Guild não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        total_events = events.count()
        event_types = events.values('type').annotate(count=Count('type'))
        players_involved = events.filter(player__isnull=False).values('player__id', 'player__user__username').distinct()
        last_activity = events.aggregate(Max('created_at'))['created_at__max']
        
        return Response({
            'guild_id': str(guild_id),
            'total_events': total_events,
            'event_types': list(event_types),
            'players_involved': list(players_involved),
            'last_activity': last_activity,
        })
