"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import FieldError
from .. import models  # UserManager, User


class ModelTests(TestCase):
    """Test Models"""
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email successful"""
        email = 'test@example.com'  # Note: example.com is reserverd for tests
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """Test email is normaized for new users"""
        sample_emails = [["test1@EXAMPLE.com", "test1@example.com"],
                         ["Test2@example.com", "Test2@example.com"],
                         ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
                         ["test4@example.COM", "test4@example.com"],]
        for email, expected in sample_emails:
            user_model = get_user_model()
            user_manager: models.UserManager = user_model.objects
            user: models.User = user_manager.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_password_required(self):
        """New users without a password raises a FieldError"""
        user_model = get_user_model()
        user_manager: models.UserManager = user_model.objects
        self.assertRaises(FieldError, user_manager.create_user,
                          'email@email.com', '')

    def test_new_user_email_required(self):
        """New users without a email raises a FieldError"""
        user_model = get_user_model()
        user_manager: models.UserManager = user_model.objects
        self.assertRaises(FieldError, user_manager.create_user, '', 'pw')

    def test_create_superuser(self):
        """Test creating a super user"""
        email = 'super@example.com'  # Note: example.com is reserverd for tests
        password = 'testpass123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
