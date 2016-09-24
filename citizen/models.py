from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class CitizenManager(BaseUserManager):
    use_in_migrations = True

    def _create_citizen(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_citizen(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_citizen(username,  password, **extra_fields)


class Citizen(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, blank=True, max_length=256)
    pkey = models.CharField(unique=True, null=True, 
        blank=False, max_length=255) # 255 characters should suffice for RSA 2048

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['pkey']

    def __unicode__(self):
        return self.username.encode("utf8")

    def get_short_name(self):
        "Returns the short name for the user."
        return self.username[0:10]

    def get_full_name(self):
        return self.username

    objects = CitizenManager()
    class Meta:
        db_table = "citizen"