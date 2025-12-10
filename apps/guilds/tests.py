import uuid
from rest_framework import status
from rest_framework.test import APITestCase
from apps.guilds.models import Guild
from django.urls import reverse
from django.contrib.auth import get_user_model


class GuildModelTests(APITestCase):
    """Tests for the Guild model and Guild API endpoints."""

    def setUp(self) -> None:
        """Set up initial data for tests."""
        self.guild1 = Guild.objects.create(
            name="Guild One",
            score="1000",
            awards=["first_win"]
        )
        self.guild2 = Guild.objects.create(
            name="Guild Two",
            score="500",
            awards=[]
        )
        # authenticate a Django auth user for write operations
        AuthUser = get_user_model()
        self.auth_user = AuthUser.objects.create_user(username="guilds_apitest_auth")
        self.client.force_authenticate(user=self.auth_user)

    # ----------------- MODEL TESTS -----------------
    def test_guild_creation(self) -> None:
        """Test creating a guild via ORM."""
        guild = Guild.objects.create(name="Test Guild", score="300", awards=["award1"])
        self.assertIsNotNone(guild.id)
        self.assertIsInstance(guild.id, uuid.UUID)
        self.assertEqual(guild.name, "Test Guild")
        self.assertEqual(guild.score, "300")
        self.assertEqual(guild.awards, ["award1"])
        self.assertIsNotNone(guild.created_at)

    def test_guild_str_representation(self) -> None:
        """Test __str__ returns the guild name."""
        self.assertEqual(str(self.guild1), "Guild One")

    def test_awards_default_list(self) -> None:
        """Test that awards default to empty list if not provided."""
        guild = Guild.objects.create(name="No Awards", score="0")
        self.assertEqual(guild.awards, [])
        self.assertIsInstance(guild.awards, list)

    def test_duplicate_names_allowed(self) -> None:
        """Two guilds can have the same name."""
        Guild.objects.create(name="Guild One", score="200")
        count = Guild.objects.filter(name="Guild One").count()
        self.assertEqual(count, 2)

    # ----------------- API TESTS -----------------
    def test_list_guilds(self) -> None:
        """Test GET /guilds/ returns all guilds."""
        url = reverse('guild-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.guild1.name)

    def test_retrieve_guild(self) -> None:
        """Test GET /guilds/{id}/ returns correct guild."""
        url = reverse('guild-detail', args=[self.guild1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.guild1.name)

    def test_create_guild(self) -> None:
        """Test POST /guilds/ creates a guild."""
        url = reverse('guild-list')
        payload = {"name": "New Guild", "score": "750", "awards": ["achievement"]}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Guild.objects.count(), 3)
        self.assertEqual(Guild.objects.get(name="New Guild").score, "750")

    def test_update_guild(self) -> None:
        """Test PUT /guilds/{id}/ updates a guild."""
        url = reverse('guild-detail', args=[self.guild1.id])
        payload = {"name": "Updated Guild", "score": "2000", "awards": ["updated"]}
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.guild1.refresh_from_db()
        self.assertEqual(self.guild1.name, "Updated Guild")
        self.assertEqual(self.guild1.score, "2000")

    def test_partial_update_guild(self) -> None:
        """Test PATCH /guilds/{id}/ partially updates a guild."""
        url = reverse('guild-detail', args=[self.guild2.id])
        payload = {"score": "900"}
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.guild2.refresh_from_db()
        self.assertEqual(self.guild2.score, "900")

    def test_delete_guild(self) -> None:
        """Test DELETE /guilds/{id}/ deletes a guild."""
        url = reverse('guild-detail', args=[self.guild1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Guild.objects.filter(id=self.guild1.id).exists())
