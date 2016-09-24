from crypto import *
from datetime import datetime, timedelta
from models import *
from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from math import floor

def dict_from_params(params):
    if params is None:
        return {}
    l = params.split("&")
    out = {}
    for args in l:
        key, val = args.split("=")
        out[key] = val
    return out


class AbstractChallenge():
    class Meta:
        abstract = True

    def generate(self):
        pass


    @staticmethod
    def validate(entry):
        time_sent = entry.sent_on
        expiry = timedelta(seconds=entry.expiry_time)
        now = timezone.now()
        return time_sent + expiry > now



class HashCash(AbstractChallenge):

    def __init__(self, bits=settings.HASHCASH_DEFAULT_BITS, salt=None,
        salt_size=settings.HASHCASH_DEFAULT_SALT_SIZE, date_pref=None):
        if type(bits) != int:
            bits = int(bits)
        self.bits = bits
        self.salt = salt
        self.salt_size = salt_size
        if date_pref is None:
            self.date_pref = "%s" % timezone.now().strftime("%Y-%m-%d-%H-%M")
        else:
            self.date_pref = date_pref


    def generate(self):
        this_salt=None
        if self.salt is None:
            this_salt = random_string(self.salt_size).replace("=", "a")
        else:
            this_salt = self.salt

        params="bits={0}&salt={1}&date_pref={2}".format(self.bits, this_salt, self.date_pref)

        """
        The citizen and sent_on attributes should be set later by the
        view that called this method. 
        """
        challenge = Challenge(ctype=ChallengeType.objects.get(ctype=0),
                              parameters=params)

        return challenge

    def check_validity(self, entry):
        hex_digits = int(floor(self.bits/4))
        stamp = "{0}:{1}:{2}".format(self.date_pref, self.salt, entry.answer)
        print sha_hash(stamp)
        return sha_hash(stamp).startswith('0'*hex_digits)


    @staticmethod
    def validate(entry):
        kwargs = dict_from_params(entry.parameters)
        h = HashCash(**kwargs)
        if not AbstractChallenge.validate(entry):
            return False
        return h.check_validity(entry)




class ChallengeFactory:

    def __init__(self, *args, **kwargs):
        self.args = args

    @staticmethod
    def new(id):
        if id == settings.HASHCASH_CHALLENGE:
            return HashCash
        else:
            raise NotImplementedError()

