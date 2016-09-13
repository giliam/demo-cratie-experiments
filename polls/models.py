from __future__ import unicode_literals

from django.db import models

from citizen.models import Citizen
from candidates.models import Candidate
# Create your models here.


class Poll(models.Model):
    name = models.CharField(max_length=255, unique=True, 
        null=False, default=False)
    description = models.CharField(max_length=10000, null=False, blank=True, 
        default="")

    class Meta:
        db_table = "poll"


class Vote(models.Model):
    poll = models.ForeignKey(Poll, null=False, blank=False)
    voter = models.ForeignKey(Citizen, null=False, blank=False, default="")
    class Meta:
        db_table = "vote"

class DataVote(models.Model):
    vote = models.ForeignKey(Vote, null=False, blank=False)
    value = models.PositiveIntegerField(null=False, default=0)
    candidate = models.ForeignKey(Candidate, null=False, blank=False)

    class Meta:
        db_table = "data_vote"