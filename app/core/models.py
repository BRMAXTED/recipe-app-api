"""
Datanase models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


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
