from typing import Any
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Count, Max, QuerySet

from apps.events.models import Event
from apps.events.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet[Any]):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> QuerySet[Event]:
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
    def statistics(self, request: Any) -> Response:
        total_events = Event.objects.count()
        response_data: dict[str, Any] = {
            'total_events': total_events,
            'events_by_type': [],
            'top_players': [],
            'top_guilds': [],
        }
        from django.db.models import QuerySet
        try:
            event_types_qs: QuerySet[Any] = Event.objects.all()
            type_counts: dict[str, int] = {}
            for event in event_types_qs:
                type_counts[event.type] = type_counts.get(event.type, 0) + 1
            response_data['events_by_type'] = [
                {'type': k, 'count': v} for k, v in type_counts.items()
            ]
            
            # Top players
            player_counts: dict[str, int] = {}
            for event in event_types_qs.filter(player__isnull=False):
                username = event.player.user.username if event.player else 'Unknown'
                player_counts[username] = player_counts.get(username, 0) + 1
            response_data['top_players'] = [
                {'player__user__username': k, 'count': v}
                for k, v in sorted(player_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            ]
            
            # Top guilds
            guild_counts: dict[str, int] = {}
            for event in event_types_qs.filter(guild__isnull=False):
                guild_name = event.guild.name if event.guild else 'Unknown'
                guild_counts[guild_name] = guild_counts.get(guild_name, 0) + 1
            response_data['top_guilds'] = [
                {'guild__name': k, 'count': v}
                for k, v in sorted(guild_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            ]
        except Exception:  # pragma: no cover
            pass
        
        return Response(response_data)
        
        return Response(response_data)

    @action(detail=False, methods=["get"])
    def player_stats(self, request: Any) -> Response:
        player_id = request.query_params.get('player_id')
        if not player_id:
            return Response(
                {'error': 'player_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        events_qs = Event.objects.filter(player_id=player_id)
        if not events_qs.exists():
            return Response(
                {'error': 'Player não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        total_events = events_qs.count()
        
        # Count event types without .annotate() to avoid mypy-django-plugin crash
        event_types: dict[str, int] = {}
        for event in events_qs:
            event_types[event.type] = event_types.get(event.type, 0) + 1
        
        # Get last activity
        last_activity = None
        for event in events_qs.order_by('-created_at')[:1]:
            last_activity = event.created_at
        
        # Get related guilds
        guilds_list: list[dict[str, Any]] = []
        guild_ids: set[Any] = set()
        for event in events_qs.filter(guild__isnull=False):
            if event.guild and event.guild.id not in guild_ids:
                guilds_list.append({
                    'guild__id': str(event.guild.id),
                    'guild__name': event.guild.name
                })
                guild_ids.add(event.guild.id)
        
        return Response({
            'player_id': str(player_id),
            'total_events': total_events,
            'event_types': [{'type': k, 'count': v} for k, v in event_types.items()],
            'last_activity': last_activity,
            'guilds_related': guilds_list,
        })

    @action(detail=False, methods=['get'])
    def guild_stats(self, request: Any) -> Response:
        guild_id = request.query_params.get('guild_id')
        if not guild_id:
            return Response(
                {'error': 'guild_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        events_qs = Event.objects.filter(guild_id=guild_id)
        if not events_qs.exists():
            return Response(
                {'error': 'Guild não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        total_events = events_qs.count()
        
        # Count event types without .annotate() to avoid mypy-django-plugin crash
        event_types: dict[str, int] = {}
        for event in events_qs:
            event_types[event.type] = event_types.get(event.type, 0) + 1
        
        # Get involved players
        players_list: list[dict[str, Any]] = []
        player_ids: set[Any] = set()
        for event in events_qs.filter(player__isnull=False):
            if event.player and event.player.id not in player_ids:
                players_list.append({
                    'player__id': str(event.player.id),
                    'player__user__username': event.player.user.username
                })
                player_ids.add(event.player.id)
        
        # Get last activity
        last_activity = None
        for event in events_qs.order_by('-created_at')[:1]:
            last_activity = event.created_at
        
        return Response({
            'guild_id': str(guild_id),
            'total_events': total_events,
            'event_types': [{'type': k, 'count': v} for k, v in event_types.items()],
            'players_involved': players_list,
            'last_activity': last_activity,
        })
