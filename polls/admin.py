from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("poll", "voter_show_name")

    def voter_show_name(self, obj):
        obj.get_short_name()

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display=("name", )

