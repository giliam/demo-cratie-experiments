from __future__ import unicode_literals

from django.db import models

from citizen.models import Citizen
# Create your models here.


class Poll(models.Model):
    name = models.CharField(max_length=255, unique=True, 
        null=False, default=False)
    description = models.CharField(max_length=10000, null=False, blank=True, 
        default="")

    class Meta:
        db_table = "poll"



class Vote(models.Model):
    value = models.PositiveIntegerField(null=False, default=0)
    poll = models.ForeignKey(Poll, null=False, blank=False)
    voter = models.ForeignKey(Citizen, null=False, blank=False, default="")
    class Meta:
        db_table = "vote"