"""
Database models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import FieldError
from django.utils.translation import gettext_lazy as translate
#  from django.contrib.postgres.fields import ArrayField


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
        unique=True,
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


class BusinessClient(models.Model):
    name = models.CharField(
        translate("Client Name"),
        max_length=150,
        unique=True,
        help_text=translate(
            "Required. 150 characters or fewer."
        ),
        error_messages={
            "unique": translate("A Client with that name already exists."),
        },)
    date_created = models.DateTimeField(translate("date created"),
                                        default=timezone.now)


class Database(models.Model):
    """
    DeltaV Database object
    """
    name = models.CharField(
        translate("Database Name"),
        max_length=150,
        unique=True,
        help_text=translate(
            "Required. 150 characters or fewer."
        ),
        error_messages={
            "unique": translate("A Database with that name already exists."),
        },)
    description = models.CharField(
        translate("Database Name"),
        max_length=200,
        help_text=translate(
            "200 characters or fewer."
        ),)
    owned_by = models.ForeignKey(
        BusinessClient,
        verbose_name=translate("Company Name"),
        on_delete=models.RESTRICT,
        max_length=200,
        help_text=translate(
            "200 characters or fewer."
        ),)
    created_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.RESTRICT,
        )
    date_created = models.DateTimeField(translate("date created"),
                                        default=timezone.now)


class Project(models.Model):
    """
    Project object
    """
    name = models.CharField(
        translate("Project Name"),
        max_length=150,
        unique=True,
        help_text=translate(
            "Required. 150 characters or fewer."
        ),
        error_messages={
            "unique": translate("A project with that name already exists."),
        },)
    description = models.CharField(
        translate("Database Name"),
        max_length=200,
        help_text=translate(
            "200 characters or fewer."
        ),)
    database = models.ForeignKey(
        Database,
        verbose_name=translate("Database Name"),
        on_delete=models.RESTRICT,
        max_length=50,
        help_text=translate(
            "Required. 50 characters or fewer."
        ),)
    client = models.ForeignKey(
        BusinessClient,
        verbose_name=translate("Client Name"),
        on_delete=models.RESTRICT,
        max_length=50,
        help_text=translate(
            "Required. 50 characters or fewer."
        ),)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
    )
    date_created = models.DateTimeField(translate("date created"),
                                        default=timezone.now)
