from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Citizen)
class CitizenAdmin(admin.ModelAdmin):
    pass



