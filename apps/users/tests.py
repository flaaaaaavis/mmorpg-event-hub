import uuid
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from apps.users.models import User
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    """Tests for the User model."""

    def test_user_creation(self):
        """Test creating a user."""
        user = User.objects.create(username="testuser")
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, "testuser")
        self.assertIsNotNone(user.created_at)

    def test_user_id_is_uuid(self):
        """Test that user ID is a UUID."""
        user = User.objects.create(username="uuiduser")
        self.assertIsInstance(user.id, uuid.UUID)

    def test_user_username_unique(self):
        """Test that usernames are unique."""
        User.objects.create(username="unique_user")
        with self.assertRaises(Exception):  # IntegrityError
            User.objects.create(username="unique_user")

    def test_user_str_representation(self):
        """Test the string representation of a user."""
        user = User.objects.create(username="display_user")
        self.assertEqual(str(user), "display_user")


class UserAPITests(APITestCase):
    """Tests for the User API endpoints."""

    def setUp(self):
        """Set up test fixtures."""
        self.user1 = User.objects.create(username="apiuser1")
        self.user2 = User.objects.create(username="apiuser2")
        # authenticate a Django auth user for write operations
        AuthUser = get_user_model()
        self.auth_user = AuthUser.objects.create_user(username="users_apitest_auth")
        self.client.force_authenticate(user=self.auth_user)

    def test_list_users(self):
        """Test GET /users/ returns all users."""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_user(self):
        """Test GET /users/{id}/ returns correct user."""
        url = reverse('user-detail', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "apiuser1")

    def test_create_user(self):
        """Test POST /users/ creates a user."""
        url = reverse('user-list')
        payload = {"username": "newuser"}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(response.data['username'], "newuser")

    def test_update_user(self):
        """Test PUT /users/{id}/ updates a user."""
        url = reverse('user-detail', args=[self.user1.id])
        payload = {"username": "updateduser"}
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, "updateduser")

    def test_partial_update_user(self):
        """Test PATCH /users/{id}/ partially updates a user."""
        url = reverse('user-detail', args=[self.user2.id])
        payload = {"username": "patcheduser"}
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.username, "patcheduser")

    def test_delete_user(self):
        """Test DELETE /users/{id}/ deletes a user."""
        url = reverse('user-detail', args=[self.user1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())

