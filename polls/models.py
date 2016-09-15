from __future__ import unicode_literals

from django.db import models
from django.forms import ValidationError

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


class ClassicMajorityPoll:
    name = "Classic majority poll"
    form_associated = MajorityPollForm
    pkey = 1

    def form_handle(self, form):
        if form.is_valid():
            vote = Vote()
            vote.poll = Poll.objects.get(id=self.pkey)
            vote.voter = 1

            dataVote = DataVote()
            dataVote.vote = vote
            dataVote.value = 1
            dataVote.candidate= form.cleaned_data["candidates"]

            vote.save()
            dataVote.save()
        else:
            raise ValidationError("Form is not valid")

class ApprovalPoll:
    name = "Approval poll"
    form_associated = ApprovalPollForm
    pkey = 2

    def form_handle(self, form):
        if form.is_valid():
            print form.cleaned_data["candidates"]
        else:
            raise ValidationError("Form is not valid")


POLLS_LIST=[ClassicMajorityPoll, ApprovalPoll]

def check_polls_lists():
    for key, poll in enumerate(POLLS_LIST):
        if key != poll().pkey-1:
            raise Exception("Couldn't validate polls list")
check_polls_lists()