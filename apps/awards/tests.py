from django.test import TestCase
from apps.awards.models import Award
from apps.events.models import Event, EventType
from apps.players.models import Player
from apps.guilds.models import Guild
from apps.users.models import User


class AwardsSignalsTests(TestCase):
    def setUp(self) -> None:
        # create users, players and guilds
        self.user_a = User.objects.create(username="user_a")
        self.user_b = User.objects.create(username="user_b")
        self.user_c = User.objects.create(username="user_c")

        self.guild1 = Guild.objects.create(name="GuildOne", score="100")
        self.guild2 = Guild.objects.create(name="GuildTwo", score="200")

        self.player_a = Player.objects.create(user=self.user_a, guild=self.guild1)
        self.player_b = Player.objects.create(user=self.user_b, guild=self.guild2)
        self.player_c = Player.objects.create(user=self.user_c, guild=self.guild1)

    def test_solo_clear_award_created(self) -> None:
        # DUNGEON_CLEAR with a single party member -> SOLO_CLEAR
        event = Event.objects.create(
            type=EventType.DUNGEON_CLEAR,
            details={"party_members": [str(self.player_a.id)], "xp_received": 500},
            player=self.player_a,
            guild=self.guild1,
        )

        self.assertTrue(
            Award.objects.filter(player=self.player_a, award_type='SOLO_CLEAR', event=event).exists()
        )

    def test_guild_harmony_award_created_for_all(self) -> None:
        # DUNGEON_CLEAR where all party members are in same guild as event.guild
        party = [str(self.player_a.id), str(self.player_c.id)]
        event = Event.objects.create(
            type=EventType.DUNGEON_CLEAR,
            details={"party_members": party, "xp_received": 1200},
            player=self.player_a,
            guild=self.guild1,
        )

        # Both players should receive GUILD_HARMONY
        self.assertTrue(Award.objects.filter(player=self.player_a, award_type='GUILD_HARMONY', event=event).exists())
        self.assertTrue(Award.objects.filter(player=self.player_c, award_type='GUILD_HARMONY', event=event).exists())

    def test_revenge_award_created(self) -> None:
        # player_b kills player_a first
        Event.objects.create(
            type=EventType.PLAYER_KILL,
            details={"target_id": str(self.player_a.id), "damage": 100},
            player=self.player_b,
            guild=self.player_b.guild,
        )

        # now player_a kills player_b -> should get REVENGE_AWARD
        event = Event.objects.create(
            type=EventType.PLAYER_KILL,
            details={"target_id": str(self.player_b.id), "damage": 200},
            player=self.player_a,
            guild=self.player_a.guild,
        )

        self.assertTrue(Award.objects.filter(player=self.player_a, award_type='REVENGE_AWARD', event=event).exists())

    def test_rival_slayer_award_created_after_two_kills(self) -> None:
        # player_b is killed twice by player_a
        Event.objects.create(
            type=EventType.PLAYER_KILL,
            details={"target_id": str(self.player_b.id), "damage": 50},
            player=self.player_a,
            guild=self.player_a.guild,
        )
        # second kill, this should trigger RIVAL_SLAYER creation
        Event.objects.create(
            type=EventType.PLAYER_KILL,
            details={"target_id": str(self.player_b.id), "damage": 80},
            player=self.player_a,
            guild=self.player_a.guild,
        )

        self.assertTrue(Award.objects.filter(player=self.player_a, award_type='RIVAL_SLAYER').exists())
        # ensure at least one RIVAL_SLAYER references the recent event or target
        rival = Award.objects.filter(player=self.player_a, award_type='RIVAL_SLAYER').first()
        self.assertIsNotNone(rival)
        assert rival is not None  # type narrowing
        self.assertIn(str(self.player_b.id), (rival.description or ""))
