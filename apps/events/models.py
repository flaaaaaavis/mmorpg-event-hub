import uuid
from django.db import models
from apps.players.models import Player
from apps.guilds.models import Guild


# Event type choices for MMORPG events
class EventType(models.TextChoices):
    PLAYER_KILL = "PLAYER_KILL", "Player Kill"
    DUNGEON_CLEAR = "DUNGEON_CLEAR", "Dungeon Clear"
    ITEM_PURCHASE = "ITEM_PURCHASE", "Item Purchase"
    GUILD_JOIN = "GUILD_JOIN", "Guild Join"
    GUILD_LEAVE = "GUILD_LEAVE", "Guild Leave"
    PLAYER_LEVEL_UP = "PLAYER_LEVEL_UP", "Player Level Up"
    QUEST_COMPLETE = "QUEST_COMPLETE", "Quest Complete"
    MARKET_TRANSACTION = "MARKET_TRANSACTION", "Market Transaction"
    OTHER = "OTHER", "Other"


class Event(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    type = models.CharField(
        max_length=50,
        choices=EventType.choices,
        default=EventType.OTHER,
        help_text="Type of event in the MMORPG (e.g., PLAYER_KILL, DUNGEON_CLEAR)"
    )
    details = models.JSONField(
        help_text="Event-specific details in JSON format"
    )
    timestamp = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Event timestamp from game server"
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="events"
    )
    guild = models.ForeignKey(
        Guild,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="events"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["type", "-created_at"]),
            models.Index(fields=["player", "-created_at"]),
            models.Index(fields=["guild", "-created_at"]),
        ]

    def __str__(self) -> str:
        return f"Event {self.id} ({self.type})"
