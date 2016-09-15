from crypto import *
from datetime import datetime, timedelta
from models import *
from django.conf import settings


def dict_from_params(params):
    if params is None:
        return {}
    l = params.split("&")
    out = {}
    for args in l:
        key, val = l.split("=")
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
        now = datetime.today()
        return time_sent + expiry > now



class HashCash(AbstractChallenge):

    def __init__(self, bits=settings.HASHCASH_DEFAULT_BITS, salt=None,
        salt_size=settings.HASHCASH_DEFAULT_SALT_SIZE):
        self.bits = bits
        self.salt = salt
        self.salt_size = salt_size
        self.date_pref = "%s" % datetime.today().strftime("%Y-%m-%d-%H-%M")


    def generate(self):
        this_salt=None
        if self.salt is None:
            this_salt = random_string(self.salt_size)
        else:
            this_salt = self.salt

        params="bits={0}&salt={1}&date_pref".format(self.bits, this_salt, self.date_pref)

        """
        The citizen and sent_on attributes should be set later by the
        view that called this method. 
        """
        challenge = Challenge(ctype=0,
                              parameters=params)

        return challenge

    def check_validity(self, entry):
        hex_digits = int(floor(self.bits/4))
        stamp = "{0}:{1}:{2}".format(self.date_pref, self.salt, entry.answer)
        return sha_hash(stamp).hexdigest().startswith('0'*hex_digits)


    @staticmethod
    def validate(entry):
        kwargs = dict_from_params(entry.params)
        h = HashCash(**kwargs)
        if not super(HashCash, h).validate(entry):
            return False
        return h.check_validity()




class ChallengeFactory:

    def __init__(self, *args, **kwargs):
        self.args = args

    @staticmethod
    def new(id):
        if id == settings.HASHCASH_CHALLENGE:
            return HashCash
        else:
            raise NotImplementedError()

