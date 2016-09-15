from django.db import models
from citizen.models import *
# Create your models here.



class ChallengeType(models.Model):
    ctype = models.PositiveIntegerField(null=False, default=0)
    cname = models.CharField(max_length=255, null=False, blank=True)



class Challenge(models.Model):
    citizen = models.ForeignKey(Citizen, null=False)
    ctype = models.ForeignKey(ChallengeType, null=False)
    answer_correct = models.BooleanField(null=False, default=False)
    answer = models.CharField(null=True, max_length=512)
    sent_on = models.DateTimeField(auto_now_add=True)
    expiry_time = models.PositiveIntegerField(null=False, default=300) # in seconds
    parameters = models.CharField(null=True, blank=True, max_length=512)

    class Meta:
        db_table = "challenge"