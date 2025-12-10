import uuid
from typing import Any, List, Optional, TYPE_CHECKING
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.events.models import Event, EventType
from apps.awards.models import Award
from apps.players.models import Player


def _get_player_by_identifier(pid: Any) -> Optional[Player]:
    if pid is None:
        return None
    if isinstance(pid, Player):
        return pid
    try:
        uid = uuid.UUID(str(pid))
        return Player.objects.filter(id=uid).first()
    except Exception:
        return Player.objects.filter(user__username=str(pid)).first()


@receiver(post_save, sender=Event)
def detect_awards_on_event(sender: Any, instance: Event, created: bool, **kwargs: Any) -> None:
    if not created:
        return
    event = instance
    try:
        if event.type == EventType.DUNGEON_CLEAR:
            party = event.details.get("party_members") if isinstance(event.details, dict) else None
            if party:
                players: List[Optional[Player]] = [_get_player_by_identifier(p) for p in party]
                players = [p for p in players if p]
                if len(players) == 1:
                    player = players[0]
                    Award.objects.get_or_create(
                        player=player,
                        award_type="SOLO_CLEAR",
                        event=event,
                        defaults={"description": "Solo dungeon clear"},
                    )
                if getattr(event, "guild", None) and players:
                    # Use getattr to avoid Pylance errors about dynamic Django attrs
                    same_guild = all(
                        (getattr(p, "guild_id", None) == getattr(event, "guild_id", None)) for p in players
                    )
                    if same_guild:
                        for p in players:
                            Award.objects.get_or_create(
                                player=p,
                                award_type="GUILD_HARMONY",
                                event=event,
                                defaults={"description": f"GuildHarmony for guild {getattr(event, 'guild_id', None)}"},
                            )
        elif event.type == EventType.PLAYER_KILL:
            killer = event.player
            target_identifier = event.details.get("target_id") if isinstance(event.details, dict) else None
            target = _get_player_by_identifier(target_identifier)
            if killer and target:
                revenge_exists = Event.objects.filter(
                    type=EventType.PLAYER_KILL,
                    player=target,
                    details__target_id=str(getattr(killer, "id", "")),
                ).exists()
                if revenge_exists:
                    Award.objects.get_or_create(
                        player=killer,
                        award_type="REVENGE_AWARD",
                        event=event,
                        defaults={"description": f"Revenge against {getattr(target, 'id', None)}"},
                    )

                kill_count = Event.objects.filter(
                    type=EventType.PLAYER_KILL, player=killer, details__target_id=str(getattr(target, "id", ""))
                ).count()
                if kill_count >= 2:
                    exists = Award.objects.filter(
                        player=killer, award_type="RIVAL_SLAYER", description__contains=str(getattr(target, "id", ""))
                    ).exists()
                    if not exists:
                        Award.objects.create(
                            player=killer,
                            award_type="RIVAL_SLAYER",
                            event=event,
                            description=f"Rival slayer of {getattr(target, 'id', None)} (kills: {kill_count})",
                        )
    except Exception:
        # Ensure signal processing never raises
        return
