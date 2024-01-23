"""
Tests for the Django admin modifications
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """
    Tests for Django Admin
    """

    def setUp(self):
        """
        Note: this function is defined from django, is executed in a
        similar fashion as __init__
        Create user and client
        """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        # https://docs.djangoproject.com/en/5.0/topics/testing/tools/#django.test.Client.force_login
        self.client.force_login(self.admin_user)
        #
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User',
        )

    def test_users_list(self):
        """
        Test that users are listed on page
        """
        # https://docs.djangoproject.com/en/dev/topics/http/urls/#reverse-resolution-of-urls
        # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#reversing-admin-urls
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """
        Test the edit user page works
        """
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_add_user_page(self):
        """
        Test the add user page works
        """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
