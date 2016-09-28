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
    key = models.PositiveIntegerField(null=False, default=0)

    def __unicode__(self):
        return self.name.encode("utf8")

    class Meta:
        db_table = "poll_type"

class Poll(models.Model):
    poll_types = models.ManyToManyField(PollType, related_name='+')
    date_beginning_poll = models.DateTimeField(auto_now=False)
    date_end_poll = models.DateTimeField(auto_now=False)

    def __unicode__(self):
        return u"Poll \"{0}\"".format(", ".join([poll.name.encode("utf8") for poll in self.poll_types.all()]))

    class Meta:
        db_table = "poll"

class Vote(models.Model):
    poll = models.ForeignKey(Poll, null=False, blank=False)
    voter = models.ForeignKey(Citizen, null=False, blank=False, default="")
    class Meta:
        db_table = "vote"

class DataVote(models.Model):
    poll = models.ForeignKey(Poll, null=False, blank=False)
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

    def has_voted(self, poll_id):
        dataVotes = Vote.objects.filter(voter__id=1, poll__id=poll_id)
        print len(dataVotes.all())

    def form_handle(self, form):
        self.has_voted(1)
        if form.is_valid():
            vote = Vote()
            vote.poll = Poll.objects.get(id=self.key)
            vote.voter = Citizen.objects.get(id=1)
            vote.save()
            return True
        else:
            raise ValidationError("Form is not valid")
            return False

    def compute_results(self, poll):
        return {}

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
            dataVote.poll = Poll.objects.get(id=self.key)
            dataVote.value = 1
            dataVote.candidate= form.cleaned_data["candidates"]
            dataVote.save()
        else:
            raise ValidationError("Form is not valid")

    def compute_results(self, poll):
        data_votes = DataVote.objects.filter(poll=poll).values("candidate__name").annotate(total_votes=models.Sum('value'))
        return data_votes

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
                dataVote.poll = Poll.objects.get(id=self.key)
                dataVote.value = 1
                dataVote.candidate = candidate
                dataVote.save()
        else:
            raise ValidationError("Form is not valid")

    def compute_results(self, poll):
        data_votes = DataVote.objects.filter(poll=poll).values("candidate__name").annotate(total_votes=models.Sum('value'))

        return {}

POLLS_LIST=[ClassicMajorityPoll, ApprovalPoll]

def check_polls_lists():
    for key, poll in enumerate(POLLS_LIST):
        if key != poll().key-1:
            raise Exception("Couldn't validate polls list")
check_polls_lists()