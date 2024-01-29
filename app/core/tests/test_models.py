"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import FieldError
from core import models  # UserManager, User


class ModelTests(TestCase):
    """Test Models"""
    def test_create_user_successful(self):
        """Test creating a user with an username successful"""
        username = 'user1'  # Note: example.com is reserverd for tests
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            username=username,
            password=password,
        )
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    # def test_new_user_email_normalize(self):
    #     """Test email is normaized for new users"""
    #     sample_emails = [["test1@EXAMPLE.com", "test1@example.com"],
    #                      ["Test2@example.com", "Test2@example.com"],
    #                      ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
    #                      ["test4@example.COM", "test4@example.com"],]
    #     for email, expected in sample_emails:
    #         user_model = get_user_model()
    #         user_manager: models.UserManager = user_model.objects
    #         user: models.User = user_manager.create_user(email, 'sample123')
    #         self.assertEqual(user.email, expected)

    def test_new_user_password_required(self):
        """New users without a password raises a FieldError"""
        user_model = get_user_model()
        user_manager: models.UserManager = user_model.objects
        self.assertRaises(FieldError, user_manager.create_user,
                          'user1', '')

    def test_new_user_username_required(self):
        """New users without a username raises a FieldError"""
        user_model = get_user_model()
        user_manager: models.UserManager = user_model.objects
        self.assertRaises(FieldError, user_manager.create_user, '', 'pw')

    def test_create_superuser(self):
        """Test creating a super user"""
        username = 'superuser1'  # Note: example.com is reserverd for tests
        password = 'testpass123'
        user = get_user_model().objects.create_superuser(
            username=username,
            password=password,
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_business_client(self):
        """Test making a business client entry"""
        business_client = models.BusinessClient.objects.create(
            name='TestClientName',
        )
        self.assertEqual(business_client.name, 'TestClientName')

    def test_create_database(self):
        """Test making a database entry"""
        user = get_user_model().objects.create_user(
            'user1',
            'testpass123'
        )
        business_client = models.BusinessClient.objects.create(
            name='TestClientName',
        )
        database = models.Database.objects.create(
            name='Database123',
            description='Sample project detailed description',
            owned_by=business_client,
            created_by=user,
        )
        self.assertEqual(database.name, 'Database123')

    def test_create_project(self):
        """Test making a project entry"""
        user = get_user_model().objects.create_user(
            'user1',
            'testpass123'
        )
        business_client = models.BusinessClient.objects.create(
            name='TestClientName',
        )
        database = models.Database.objects.create(
            name='Database123',
            description='Sample Database detailed description',
            owned_by=business_client,
            created_by=user
        )
        project = models.Project.objects.create(
            name='Project123',
            description='Sample project detailed description',
            database=database,
            business_client=business_client,
            created_by=user
        )

        self.assertEqual(project.name, 'Project123')
