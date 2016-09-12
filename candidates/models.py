from __future__ import unicode_literals

from django.db import models

# Create your models here.



class Party(models.Model):
    name = models.CharField(unique=True, null=False, default="", 
            blank=False, max_length=255)

    # Probably much more fields to come e.g. information on the party
    # (date of creation, number of adherent, number of counties, regions, numbers
    # of chairs in the assemble, previous election results etc...

    class Meta:
        db_table = "party"


class Candidate(models.Model):
    name = models.CharField(unique=True, null=False, default="", 
            blank=False, max_length=255)

    party = models.ForeignKey(Party, null=False)

    class Meta:
        db_table = "candidate"


