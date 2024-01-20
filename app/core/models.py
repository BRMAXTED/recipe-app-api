"""
Datanase models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manage for users"""

    def create_user(self, email: models.EmailField, password=None,
                    **extra_fields):
        """Create save and return a new user"""
        user: AbstractBaseUser = self.model(email=email, **extra_fields)
        user.set_password(password)
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
