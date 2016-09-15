from __future__ import unicode_literals

from django.db import models

from forms import MajorityPollForm, ApprovalPollForm

from citizen.models import Citizen
from candidates.models import Candidate
# Create your models here.

class PollType(models.Model):
    name = models.CharField(max_length=255, unique=True, 
        null=False, default=False)
    description = models.CharField(max_length=10000, null=False, blank=True, 
        default="")

    class Meta:
        db_table = "poll_type"


class ClassicMajorityPoll:
    name = "Classic majority poll"
    form_associated = MajorityPollForm

class ApprovalPoll:
    name = "Approval poll"
    form_associated = ApprovalPollForm


class Vote(models.Model):
    poll = models.ForeignKey(PollType, null=False, blank=False)
    voter = models.ForeignKey(Citizen, null=False, blank=False, default="")
    class Meta:
        db_table = "vote"

class DataVote(models.Model):
    vote = models.ForeignKey(Vote, null=False, blank=False)
    value = models.PositiveIntegerField(null=False, default=0)
    candidate = models.ForeignKey(Candidate, null=False, blank=False)

    class Meta:
        db_table = "data_vote"


POLLS_LIST=[ClassicMajorityPoll, ApprovalPoll]