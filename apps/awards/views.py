from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count

from apps.awards.models import Award
from apps.awards.serializers import AwardSerializer


class AwardViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar méritos de jogadores.
    """
    queryset = Award.objects.all()
    serializer_class = AwardSerializer

    def get_queryset(self):
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
    def leaderboard(self, request):
        """Retorna ranking de jogadores por quantidade de méritos."""
        top_players = Award.objects.values('player__user__username', 'player__id').annotate(
            awards_count=Count('id')
        ).order_by('-awards_count')[:20]
        
        return Response(list(top_players))
