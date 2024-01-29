"""
Test for client API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import BusinessClient
from client.serializers import ClientSerializer
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import (
    AbstractBaseUser,
)


CLIENT_LIST_URL = reverse('client:list')


def create_user(**params) -> AbstractBaseUser:
    """
    Create and return a new user
    """
    return get_user_model().objects.create_user(**params)


def create_client(name: str):
    client = BusinessClient.objects.create(name)
    return client


class PublicUserApiTests(TestCase):
    """
    Test the public features of the user API
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test authentication is rquired for users
        """
        res = self.client.get(CLIENT_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateClientrApiTest(TestCase):
    """
    Test API requests that require authentication
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testUser',
            password='testpass123',
            first_name='Test',
            last_name='Name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_auth_required(self):
        """
        Test authentication is rquired for users
        """
        res = self.client.get(CLIENT_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_client_success(self):
        """Test making a business client entry"""
        business_client = BusinessClient.objects.create(
            name='TestClientName',
        )
        self.assertEqual(business_client.name, 'TestClientName')

    def test_retrieve_client_list_success(self):
        """
        Test retrieving profile for logged in user
        """
        create_client('TestClient1')
        create_client('TestClient2')
        create_client('TestClient3')
        res = self.client.get(CLIENT_LIST_URL)

        clients = BusinessClient.objects.all().order_by('-id')
        serializer = ClientSerializer(clients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
