from typing import Any
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, QuerySet

from apps.awards.models import Award
from apps.awards.serializers import AwardSerializer


class AwardViewSet(viewsets.ModelViewSet[Any]):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer

    def get_queryset(self) -> QuerySet[Award]:
        queryset = Award.objects.all()
        
        # Filtro por jogador
        player_id = self.request.query_params.get('player_id')
        if player_id:
            queryset = queryset.filter(player_id=player_id)
        
        # Filtro por tipo de prêmio
        award_type = self.request.query_params.get('award_type')
        if award_type:
            queryset = queryset.filter(award_type=award_type)
        
        return queryset

    @action(detail=False, methods=['get'])
    def leaderboard(self, request: Any) -> Response:
        player_awards: dict[str, dict[str, Any]] = {}
        for award in Award.objects.all():
            if award.player:
                key = award.player.user.username
                if key not in player_awards:
                    player_awards[key] = {
                        'player__user__username': key,
                        'player__id': str(award.player.id),
                        'awards_count': 0
                    }
                player_awards[key]['awards_count'] += 1
        
        # Sort and return top 20
        sorted_players = sorted(
            player_awards.values(),
            key=lambda x: x['awards_count'],
            reverse=True
        )[:20]
        
        return Response(sorted_players)
