from django.forms import ModelForm

from models import *


class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ["value", "poll"]


    def clean(self):
        super(VoteForm, self).clean()

        



