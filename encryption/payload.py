from crypto import *
from json import loads

from django.conf import settings
# https://pypi.python.org/pypi/pycrypto

# References:
# --------to add


# Structure of a payload:
#               Payload blob
# |---------------------------------------|
# |-------------------------|-------------|
#             data             signature
# 
# 
# data: json formatted text containing the data necessary for 
# the sollicited API endpoint, encrypted with AES

# signature: RSA encrypted padded hash. For the moment the hash is 
# a SHA256 hash of the data for integrity check. 
# The padding is the AES_PWD_SIZE characters random password 
# used for data's AES encryption.
# 
# 
#            decrypted signature
# |---------------------------------------|
# |------|--------------------------------|
#   pwd              hash256


class Payload(object):

    def __init__(self, raw_content):
        """
        :str raw_content: the raw content of the http request body
        :Server server: the authority server instance for the current session
            used to retrieve the RSA key
        """
        self.blob = raw_content


    def check_validity(self):
        d = None
        enc_data = None
        enc_sig = None
        try:
            d = loads(self.blob)
            enc_data = d["data"]
            enc_sig = d["signature"]
        except ValueError, KeyError:
            return False

        dec_sig = rsa_decrypt(enc_sig, settings.SERVER_KEY)
        if len(dec_sig) != settings.SHA_SIZE + settings.AES_PWD_SIZE:
            return False
        
        pwd = dec_sig[0:32]
        h = dec_sig[32:-1]

        dec_data = aes_decrypt(enc_data, pwd)

        if sha_hash(data) != h:
            return False


        return True








