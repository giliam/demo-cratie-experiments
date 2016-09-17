# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest
from django.forms import ValidationError

from django.views.decorators.csrf import csrf_exempt
from functools import wraps

from forms import *
from models import Poll, POLLS_LIST
# Create your views here.

from encryption.payload import *


def func_badrequest(msg):
    return HttpResponseBadRequest(msg)


def check_length(request, size, **kwargs):
    return len(request.body) <= size # I don't want to do that, because I don't want to
    # download the whole body if to big. Problem is I can't just do request.read(size+1)
    # because I wouldn't be able to access request.body later on in the view function
    # Something to do with the content-length header and django middleware classes
    # http://stackoverflow.com/questions/5554952/how-do-i-get-the-content-length-of-a-django-response-object


def get_citizen_from_request(request):
    #TODO when the citizen model has been implemented

    return "a"



def check_payload(request):
    citizen = get_citizen_from_request(request)
    if citizen is None:
        return False
    # pkey = citizen.pkey
    # payload = Payload(request.body, pkey)
    # return payload.check_validity()
    return users[citizen] == 1



"""
    Checks whether the citizen's account has been validated according to a specific 
    process yet to define.
"""
def citizen_validation(view_func):
    print "citizen validation"
    def _wrapper(request, *args, **kwargs):
        # TODO
        return view_func(request, *args, **kwargs)
    return _wrapper


def request_passes_test(test_func, *args, **kwargs):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_func(request, *_args, **_kwargs):
            if test_func(request, *args, **kwargs):
                return view_func(request, *_args, **_kwargs)
            else:
                return func_badrequest("")
        return _wrapped_func
    return decorator





# def payload_validator(api_func):

#     @wraps(api_func)
#     def crypto_error(r):
#         return HttpResponseBadRequest("Erreur crypto")

#     return api_func

@csrf_exempt
@citizen_validation
@request_passes_test(check_length, 10)
@request_passes_test(check_payload)
def test_length(request, **kwargs):
    return HttpResponse(request.body)


def vote(request):
    if request.POST is None:
        return HttpResponseBadRequest('') # find a fancy error explanation

    form_vote = PollForm(request.POST)
    try:
        form_vote.save()
    except ValidationError:
        return HttpResponseBadRequest("Erreur de validation")


    return HttpResponse("A voté")


def display_vote(request, poll_id):
    poll_id = int(poll_id)
    print poll_id
    if poll_id > len(POLLS_LIST) or poll_id == 0:
        return HttpResponseBadRequest("This poll type doesn't exist.")
    poll_id = poll_id - 1
    poll_type = POLLS_LIST[poll_id]()

    if request.POST:
        form_vote = poll_type.form_associated(request.POST)
        try:
            poll_type.form_handle(form_vote)
        except ValidationError:
            return HttpResponseBadRequest("Erreur de validation")
    else:
        form_vote = poll_type.form_associated()

    return render(request, 'polls/vote.html', {'form_vote':form_vote})

def display_polls(request):
    return render(request, 'polls/polls_list.html', {'polls_list':POLLS_LIST})


"""
    Probably too costly to really compute each time there is a request.
    We should implement a cache for that.
"""
def get_results(request):
    polls = Poll.objects.all()
    results = []
    dic = {}
    for poll in polls:
        for poll_type in poll.poll_types.all():
            dic["poll"] = poll
            dic["candidates"] = POLLS_LIST[poll_type.key - 1]().compute_results(poll)
            results.append(dic)
    print results
    return render(request, 'polls/results.html', {'results':results})
