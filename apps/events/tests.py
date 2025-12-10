import uuid

from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.events.models import Event, EventType
from apps.players.models import Player
from apps.guilds.models import Guild
from apps.users.models import User
from django.contrib.auth import get_user_model


class EventModelTests(APITestCase):
    """Tests for the Event model."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.user = User.objects.create(username="testuser")
        self.guild = Guild.objects.create(name="Test Guild", score="100")
        self.player = Player.objects.create(user=self.user, guild=self.guild)

    def test_event_creation(self) -> None:
        """Test creating an event with all fields."""
        event = Event.objects.create(
            type=EventType.PLAYER_LEVEL_UP,
            details={"level": 42, "rewards": ["sword"]},
            player=self.player,
            guild=self.guild,
        )
        self.assertEqual(event.type, EventType.PLAYER_LEVEL_UP)
        self.assertIsNotNone(event.id)
        self.assertIsNotNone(event.created_at)
        self.assertEqual(event.details["level"], 42)

    def test_event_creation_minimal(self) -> None:
        """Test creating an event with only required fields (type and details)."""
        event = Event.objects.create(
            type=EventType.GUILD_JOIN,
            details={"guild_name": "New Guild"},
        )
        self.assertEqual(event.type, EventType.GUILD_JOIN)
        self.assertIsNone(event.player)
        self.assertIsNone(event.guild)

    def test_event_id_is_uuid(self) -> None:
        """Test that event ID is a UUID."""
        event = Event.objects.create(
            type=EventType.OTHER,
            details={},
        )
        self.assertIsInstance(event.id, uuid.UUID)

    def test_event_str_representation(self) -> None:
        """Test the string representation of an event."""
        event = Event.objects.create(
            type=EventType.PLAYER_KILL,
            details={"cause": "dragon"},
        )
        expected = f"Event {event.id} ({EventType.PLAYER_KILL})"
        self.assertEqual(str(event), expected)


class EventViewSetTests(APITestCase):
    """Tests for the Event API ViewSet."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.client = APIClient()
        self.user = User.objects.create(username="apiuser")
        self.guild = Guild.objects.create(name="API Guild", score="500")
        self.player = Player.objects.create(user=self.user, guild=self.guild)
        self.event = Event.objects.create(
            type=EventType.PLAYER_LEVEL_UP,
            details={"level": 50},
            player=self.player,
            guild=self.guild,
        )
        # authenticate a Django auth user for write operations
        AuthUser = get_user_model()
        self.auth_user = AuthUser.objects.create_user(username="events_apitest_auth")
        self.client.force_authenticate(user=self.auth_user)

    def test_list_events(self) -> None:
        """Test retrieving a list of all events."""
        response = self.client.get("/api/events/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["type"], EventType.PLAYER_LEVEL_UP)

    def test_create_event(self) -> None:
        """Test creating an event via POST."""
        payload = {
            "type": EventType.OTHER,
            "details": {"opponent": "Enemy Guild"},
            "player": None,
            "guild": str(self.guild.id),
        }
        response = self.client.post("/api/events/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["type"], EventType.OTHER)
        self.assertIsNotNone(response.data["id"])

    def test_retrieve_event(self) -> None:
        """Test retrieving a single event by ID."""
        url = f"/api/events/{self.event.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["type"], EventType.PLAYER_LEVEL_UP)

    def test_update_event_full(self) -> None:
        """Test full update (PUT) of an event."""
        url = f"/api/events/{self.event.id}/"
        payload = {
            "type": EventType.OTHER,
            "details": {"level": 49},
            "player": str(self.player.id),
            "guild": None,
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["type"], EventType.OTHER)

    def test_update_event_partial(self) -> None:
        """Test partial update (PATCH) of an event."""
        url = f"/api/events/{self.event.id}/"
        payload = {
            "details": {"level": 51, "bonus": "gold"},
        }
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["details"]["level"], 51)
        self.assertEqual(response.data["details"]["bonus"], "gold")

    def test_delete_event(self) -> None:
        """Test deleting an event."""
        event_id = self.event.id
        url = f"/api/events/{event_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=event_id).exists())

    def test_list_events_ordered_by_created_at(self) -> None:
        """Test that events are ordered by created_at descending."""
        Event.objects.create(type="event2", details={})
        Event.objects.create(type="event3", details={})
        response = self.client.get("/api/events/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that events are in reverse chronological order
        types = [e["type"] for e in response.data]
        self.assertEqual(types[0], "event3")  # Most recent first
