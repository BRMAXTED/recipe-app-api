"""
Test for the user api
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from user.serializers import UserDetailAdminSerializer


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')
MANAGE_URL = reverse('user:manage-list')


def get_reverse_user_id(user_id: int):
    # NOTE -detail is required due to the router
    # adding -detail after the basename
    return reverse('user:manage-detail', args=[user_id])


def create_user(**params) -> AbstractBaseUser:
    """
    Create and return a new user
    """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    Test the public features of the user API
    """

    def setUp(self):
        self.client = APIClient()

    def test_user_with_username_exists_error(self):
        """
        Test error returned if user with email exists
        """
        payload = {
            'username': 'testUser3',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'newuser'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """
        Test an error is returned if pasword less than 5 chars
        """
        payload = {
            'username': 'testUserr',
            'password': 'pw',
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            username=payload['username']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """
        Test generates token for valid credentials
        """
        user_details = {
            'username': 'testuser',
            'email': 'test@example.come',
            'password': 'test-user-password123'
        }
        create_user(**user_details)
        payload = {
            'username': user_details['username'],
            'password': user_details['password']
            }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """
        Test returns error if credentials invalid
        """
        create_user(username='exampleuser', password='goodpass')
        payload = {
            'username': 'exampleuser',
            'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_password(self):
        """
        Test returns error if credentials invalid
        """
        create_user(username='exampleuser', password='goodpass')
        payload = {
            'username': 'exampleuser',
            'password': ''}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        Test authentication is rquired for users
        """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """
    Test API requests that require authentication
    """

    def setUp(self):
        self.user = create_user(
            username='testUser',
            password='testpass123',
            first_name='Test',
            last_name='Name'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """
        Test retrieving profile for logged in user
        """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        })

    def test_post_me_not_allowed(self):
        """
        Test POST is not allowed for the me endpoint
        """
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_password(self):
        """
        Test updating the user password for the authenticated user
        """
        payload = {
            'password': 'newpassword123',
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateAdminUserApiTest(TestCase):
    """
    Test API requests that require authentication
    """

    def setUp(self):
        self.user = create_user(
            username='testUser',
            password='testpass123',
            first_name='Test',
            last_name='Name'
        )
        self.super_user = get_user_model().objects.create_superuser(
            username='testSuperUser',
            password='testpass123',
            first_name='Test',
            last_name='Name',)
        self.client = APIClient()
        self.client.force_authenticate(user=self.super_user)

    def test_create_user_as_admin(self):
        """
        Test creating a user is successful
        """
        payload = {
            'username': 'userAPI1',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'last'
        }
        res = self.client.post(MANAGE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(username=payload['username'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_get_user_as_admin(self):
        """
        Test getting a user is successful
        """
        _id = self.user.id
        user_url = get_reverse_user_id(_id)
        res = self.client.get(user_url)
        serializer = UserDetailAdminSerializer(self.user)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)
