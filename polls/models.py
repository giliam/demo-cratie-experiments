from __future__ import unicode_literals

from django.db import models
from django.forms import ValidationError

from forms import PollForm, MajorityPollForm, ApprovalPollForm

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


class AbstractPoll(object):
    name = "Abstract poll"
    form_associated = PollForm
    key = 0
    
    def __init__(self):
        pass

    def form_handle(self, form):
        if form.is_valid():
            vote = Vote()
            vote.poll = PollType.objects.get(id=self.key)
            vote.voter = Citizen.objects.get(id=1)
            vote.save()
            return vote
        else:
            raise ValidationError("Form is not valid")
            return None

class ClassicMajorityPoll(AbstractPoll):
    name = "Classic majority poll"
    form_associated = MajorityPollForm
    key = 1

    def __init__(self):
        AbstractPoll.__init__(self)

    def form_handle(self, form):
        vote = super(ClassicMajorityPoll, self).form_handle(form)
        if vote:
            dataVote = DataVote()
            dataVote.vote = vote
            dataVote.value = 1
            dataVote.candidate= form.cleaned_data["candidates"]
            dataVote.save()
        else:
            raise ValidationError("Form is not valid")

class ApprovalPoll(AbstractPoll):
    name = "Approval poll"
    form_associated = ApprovalPollForm
    key = 2

    def __init__(self):
        AbstractPoll.__init__(self)

    def form_handle(self, form):
        vote = super(ApprovalPoll, self).form_handle(form)
        if vote:
            for candidate in form.cleaned_data["candidates"]:
                print candidate
                dataVote = DataVote()
                dataVote.vote = vote
                dataVote.value = 1
                dataVote.candidate = candidate
                dataVote.save()
        else:
            raise ValidationError("Form is not valid")


POLLS_LIST=[ClassicMajorityPoll, ApprovalPoll]

def check_polls_lists():
    for key, poll in enumerate(POLLS_LIST):
        if key != poll().key-1:
            raise Exception("Couldn't validate polls list")
check_polls_lists()