import uuid
from django.db import models
from apps.players.models import Player
from apps.guilds.models import Guild

# Create your models here.
class Event(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    type = models.CharField(max_length=100)
    details = models.JSONField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True, related_name="events")
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE, null=True, blank=True, related_name="events")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event {self.id} ({self.type})"
