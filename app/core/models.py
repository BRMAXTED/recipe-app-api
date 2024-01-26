"""
Database models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import FieldError
from django.utils.translation import gettext_lazy as translate
from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):
    """Manage for users"""

    def create_user(self, username: models.CharField, password=None,
                    **extra_fields):
        """Create save and return a new user"""
        if not password:
            raise FieldError('No Password provided')
        if not username:
            raise FieldError('No username provided')
        #  normal_email = self.normalize_email(email)
        user: AbstractBaseUser = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username: models.CharField, password=None,
                         **extra_fields):
        """Create and save and return a super user"""
        extra_fields = {**extra_fields, "is_staff": True,
                        "is_superuser": True}
        user = self.create_user(username=username,
                                password=password,
                                **extra_fields)
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User in the system
    Note default django user implementation uses a username
    and password. The code implementation here replaces this
    with an email and password requirement
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        translate("username"),
        max_length=150,
        primary_key=True,
        help_text=translate(
            "Required. 150 characters or fewer. Letters, "
            "digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": translate("A user with that username already exists."),
        },
    )
    first_name = models.CharField(translate("first name"),
                                  max_length=150,
                                  blank=True)
    last_name = models.CharField(translate("last name"),
                                 max_length=150,
                                 blank=True)
    email = models.EmailField(translate("email address"), blank=True)
    databases = ArrayField(models.CharField(blank=True,
                                            max_length=20),
                           default=list,
                           verbose_name=translate("databases"))
    is_staff = models.BooleanField(
        translate("staff status"),
        default=False,
        help_text=translate("Designates whether the user "
                            "can log into this admin site."),
    )
    is_active = models.BooleanField(
        translate("active"),
        default=True,
        help_text=translate(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_created = models.DateTimeField(translate("date created"),
                                        default=timezone.now)

    objects: BaseUserManager = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
