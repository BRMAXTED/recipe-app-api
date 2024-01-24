"""
Database models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.exceptions import FieldError


class UserManager(BaseUserManager):
    """Manage for users"""

    def create_user(self, email: models.EmailField, password=None,
                    **extra_fields):
        """Create save and return a new user"""
        if not password:
            raise FieldError('No Password provided')
        if not email:
            raise FieldError('No email provided')
        normal_email = self.normalize_email(email)
        user: AbstractBaseUser = self.model(email=normal_email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email: models.EmailField, password=None,
                         **extra_fields):
        """Create and save and return a super user"""
        extra_fields = {**extra_fields, "is_staff": True,
                        "is_superuser": True}
        user = self.create_user(email=email, password=password, **extra_fields)
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User in the system
    Note default django user implementation uses a username
    and password. The code implementation here replaces this
    with an email and password requirement
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    objects: BaseUserManager = UserManager()
