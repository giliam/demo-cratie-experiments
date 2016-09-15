from django import forms

from candidates.models import Candidate


class PollForm(forms.Form):
    value = forms.IntegerField()

class MajorityPollForm(forms.Form):
    candidates = forms.ModelChoiceField(queryset=Candidate.objects.all())

class ApprovalPollForm(forms.Form):
    candidates = forms.ModelMultipleChoiceField(queryset=Candidate.objects.all())