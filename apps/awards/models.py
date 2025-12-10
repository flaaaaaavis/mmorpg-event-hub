import uuid
from django.db import models
from apps.players.models import Player
from apps.events.models import Event


class Award(models.Model):    
    AWARD_TYPES = (
        ('GUILD_HARMONY', 'Guild Harmony'),
        ('SOLO_CLEAR', 'Solo Clear'),
        ('REVENGE_AWARD', 'Revenge Award'),
        ('RIVAL_SLAYER', 'Rival Slayer'),
    )
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='awards_earned'
    )
    award_type = models.CharField(
        max_length=20,
        choices=AWARD_TYPES
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='awards_granted'
    )
    description = models.TextField(blank=True)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-earned_at']
        unique_together = ('player', 'award_type', 'event')
    
    def __str__(self) -> str:
        return f"Award {self.award_type} for {self.player}"

