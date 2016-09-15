from functools import wraps
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseForbidden

from datetime import datetime
from challenge import *
from models import *
from citizen.models import *

import json


def send_challenge(challenge_type, request, *args, **kwargs):

    if request.user is None:
        return HttpForbidden("please log in")
    ch = ChallengeFactory.new(challenge_type)(*args, **kwargs)
    new_entry = ch.generate()

    new_entry.citizen = request.user
    new_entry.sent_on = datetime.today()

    new_entry.save()


    return HttpResponse(json.dumps({"challenge": new_entry.pk,
        "challenge_params": new_entry.params}))





def solve_challenge(challenge_type, *args, **kwargs):
    """
    Generates a decorator that checks if the request has set the 
    attributes "challenge" and "answer". If not, send a challenge to
    be solved for the data to be effectively posted. If it is, checks 
    that the challenge has been correctly answered, within the right 
    time frame. If it is, allow access to the wrapped view.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request):
            challenge_answer = None
            challenge_id = None
            try:
                challenge_answer = request.POST["answer"]
                challenge_id = request.POST["challenge"]
            except KeyError:
                return send_challenge(challenge_type, request, *args, 
                    **kwargs)

            entry = Challenge.objects.get(pk=challenge_id)
            if entry is None:
                return send_challenge(challenge_type, request, *args, 
                    **kwargs)

            entry.answer = challenge_answer
            if ChallengeFactory.new(challenge_type).validate(entry):
                return view_func(request)
            else:
                return send_challenge(challenge_type, request, *args, 
                    **kwargs)
        return _wrapped

    return decorator



