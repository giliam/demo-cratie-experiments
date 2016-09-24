from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ("name",)



@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("name", "party")