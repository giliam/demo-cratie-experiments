from django.forms import ModelForm, ValidationError

from models import *
from encryption.crypto import *

class CitizenForm(ModelForm):
    class Meta:
        model = Citizen
        fields = ["password", "pkey"]
        exclude = ["username"]

    def clean_pkey(self):
        pkey = self.cleaned_data["pkey"]
        if rsa_check(rsa_recompose(pkey)):
            return rsa_clean(pkey)
        print "rsa check failed"
        raise ValidationError("Incorrect format for Public Key")
