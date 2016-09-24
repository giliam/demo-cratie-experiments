from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(ChallengeType)
class ChallengeTypeAdmin(admin.ModelAdmin):

    list_display=("ctype", "cname")


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display=("ctype", "answer_correct", "sent_on")