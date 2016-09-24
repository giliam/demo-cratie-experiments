from __future__ import unicode_literals

from django.db import models

# Create your models here.



class Party(models.Model):
    name = models.CharField(unique=True, null=False, default="", 
            blank=False, max_length=255)

    # Probably much more fields to come e.g. information on the party
    # (date of creation, number of adherent, number of counties, regions, numbers
    # of chairs in the assemble, previous election results etc...

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "party"
        verbose_name_plural = "Parties"


class Candidate(models.Model):
    name = models.CharField(unique=True, null=False, default="", 
            blank=False, max_length=255)

    party = models.ForeignKey(Party, null=False)
    
    def __repr__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "candidate"


