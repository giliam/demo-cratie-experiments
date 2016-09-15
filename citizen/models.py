from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
# Create your models here.



class Citizen(AbstractBaseUser):
    username = models.CharField(unique=True, blank=True, max_length=256)
    pkey = models.CharField(unique=True, null=True, 
        blank=False, max_length=255) # 255 characters should suffice for RSA 2048


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['pkey']

    def __unicode__(self):
        return self.username.encode("utf8")

    class Meta:
        db_table = "citizen"