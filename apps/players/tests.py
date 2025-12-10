import uuid
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from apps.players.models import Player
from apps.guilds.models import Guild
from apps.users.models import User
from django.contrib.auth import get_user_model


class PlayerModelTests(TestCase):
    """Tests for the Player model."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.user = User.objects.create(username="playeruser")
        self.guild = Guild.objects.create(name="Player Guild", score="200")

    def test_player_creation(self) -> None:
        """Test creating a player."""
        player = Player.objects.create(user=self.user, guild=self.guild)
        self.assertIsNotNone(player.id)
        self.assertEqual(player.user, self.user)
        self.assertEqual(player.guild, self.guild)
        self.assertEqual(player.awards, [])
        self.assertIsNotNone(player.created_at)

    def test_player_id_is_uuid(self) -> None:
        """Test that player ID is a UUID."""
        player = Player.objects.create(user=self.user)
        self.assertIsInstance(player.id, uuid.UUID)

    def test_player_guild_nullable(self) -> None:
        """Test creating a player without a guild."""
        player = Player.objects.create(user=self.user, guild=None)
        self.assertIsNone(player.guild)

    def test_player_str_representation(self) -> None:
        """Test the string representation of a player."""
        player = Player.objects.create(user=self.user)
        expected = f"Player {player.id}"
        self.assertEqual(str(player), expected)

    def test_player_awards_default(self) -> None:
        """Test that awards default to an empty list."""
        player = Player.objects.create(user=self.user)
        self.assertEqual(player.awards, [])
        self.assertIsInstance(player.awards, list)


class PlayerAPITests(APITestCase):
    """Tests for the Player API endpoints."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")
        self.guild = Guild.objects.create(name="Test Guild", score="500")
        self.player1 = Player.objects.create(
            user=self.user1,
            guild=self.guild,
            awards=["award1"]
        )
        self.player2 = Player.objects.create(
            user=self.user2,
            guild=None,
            awards=[]
        )
        # authenticate a Django auth user for write operations (DRF permission checks)
        AuthUser = get_user_model()
        self.auth_user = AuthUser.objects.create_user(username="apitestauth")
        self.client.force_authenticate(user=self.auth_user)

    def test_list_players(self) -> None:
        """Test GET /players/ returns all players."""
        url = reverse('player-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_player(self) -> None:
        """Test GET /players/{id}/ returns correct player."""
        url = reverse('player-detail', args=[self.player1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['awards'], ["award1"])

    def test_create_player(self) -> None:
        """Test POST /players/ creates a player."""
        url = reverse('player-list')
        payload = {
            "user": self.user1.id,
            "guild": self.guild.id,
            "awards": ["new_award"]
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 3)

    def test_update_player(self) -> None:
        """Test PUT /players/{id}/ updates a player."""
        url = reverse('player-detail', args=[self.player1.id])
        payload = {
            "user": self.user2.id,
            "guild": None,
            "awards": ["updated"]
        }
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.player1.refresh_from_db()
        self.assertEqual(self.player1.awards, ["updated"])

    def test_partial_update_player(self) -> None:
        """Test PATCH /players/{id}/ partially updates a player."""
        url = reverse('player-detail', args=[self.player2.id])
        payload = {"awards": ["new_achievement"]}
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.player2.refresh_from_db()
        self.assertEqual(self.player2.awards, ["new_achievement"])

    def test_delete_player(self) -> None:
        """Test DELETE /players/{id}/ deletes a player."""
        url = reverse('player-detail', args=[self.player1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Player.objects.filter(id=self.player1.id).exists())
