from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from encryption.crypto import *
from forms import *
from django.contrib.auth import login




@csrf_exempt
def create(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Should be post")
    print request.POST
    print request.POST["password"]
    citizen_form = CitizenForm(request.POST)
    if citizen_form.is_valid():
        print "form is valid"
        citizen = citizen_form.save()
        citizen.username = sha_hash(citizen_form.cleaned_data["pkey"])
        citizen.save()
        print "trying to login"
        login(request, citizen)
        print "trying to send response"
        return HttpResponse("Bienvenu")
    else:
        return HttpResponseBadRequest(citizen_form.errors)

