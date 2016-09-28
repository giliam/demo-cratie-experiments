from __future__ import unicode_literals

from django.db import models
from django.forms import ValidationError

from forms import PollForm, MajorityPollForm, ApprovalPollForm

from citizen.models import Citizen
from candidates.models import Candidate

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
    poll_type = models.ForeignKey(PollType, null=False, blank=False)
    voter = models.ForeignKey(Citizen, null=False, blank=False, default="")
    class Meta:
        db_table = "vote"

class DataVote(models.Model):
    poll = models.ForeignKey(Poll, null=False, blank=False)
    poll_type = models.ForeignKey(PollType, null=False, blank=False)
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

    def form_handle(self, form, voter_id, poll_id):
        if form.is_valid():
            vote = Vote()
            vote.poll = Poll.objects.get(id=poll_id)
            vote.poll_type = PollType.objects.get(key=self.key)
            vote.voter = Citizen.objects.get(id=voter_id)
            vote.save()
            return True
        else:
            print "Form is not valid"
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

    def form_handle(self, form, voter_id, poll_id):
        vote = super(ClassicMajorityPoll, self).form_handle(form, voter_id, poll_id)
        if vote:
            dataVote = DataVote()
            dataVote.poll = Poll.objects.get(id=poll_id)
            dataVote.poll_type = PollType.objects.get(key=self.key)
            dataVote.value = 1
            dataVote.candidate= form.cleaned_data["candidates"]
            dataVote.save()
        else:
            print "Form is not valid"
            raise ValidationError("Form is not valid")

    def compute_results(self, poll):
        data_votes = DataVote.objects.filter(poll=poll, poll_type__key=self.key).values("candidate__name").annotate(total_votes=models.Sum('value'))
        return data_votes

class ApprovalPoll(AbstractPoll):
    name = "Approval poll"
    form_associated = ApprovalPollForm
    key = 2

    def __init__(self):
        AbstractPoll.__init__(self)

    def form_handle(self, form, voter_id, poll_id):
        vote = super(ApprovalPoll, self).form_handle(form, voter_id, poll_id)
        if vote:
            for candidate in form.cleaned_data["candidates"]:
                dataVote = DataVote()
                dataVote.poll = Poll.objects.get(id=poll_id)
                dataVote.poll_type = PollType.objects.get(key=self.key)
                dataVote.value = 1
                dataVote.candidate = candidate
                dataVote.save()
        else:
            print "Form is not valid"
            raise ValidationError("Form is not valid")

    def compute_results(self, poll):
        data_votes = DataVote.objects.filter(poll=poll, poll_type__key=self.key).values("candidate__name").annotate(total_votes=models.Sum('value'))
        return data_votes

POLLS_LIST=[ClassicMajorityPoll, ApprovalPoll]

def check_polls_lists():
    for key, poll in enumerate(POLLS_LIST):
        if key != poll().key-1:
            print "Couldn't validate polls list"
            raise Exception("Couldn't validate polls list")
check_polls_lists()