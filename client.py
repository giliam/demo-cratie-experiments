# -*- coding: utf-8 -*-
import requests as req


# creating user

from encryption.crypto import *
from Crypto.PublicKey import RSA
from encryption.crypto import sha_hash
from math import ceil
from json import loads


def solve(date, salt, bits):
    counter = 0
    hex_digits = int(ceil(bits/4.))
    zeros = '0'*hex_digits
    while 1:
        digest = sha_hash("{0}:{1}:{2}".format(date, salt, hex(counter)[2:]))
        if digest[:hex_digits] == zeros:
            return hex(counter)[2:]
        counter += 1



SERVER = "http://localhost:8000/"

password = random_string(20)

key = RSA.generate(1024)
pkey = key.publickey().exportKey()

pkey = "".join(pkey.split("\n")[1:-1])

print "creating user {0} {1}".format(password, pkey)
r = req.post(SERVER + "citizen/create/", data={"password":password, 
    "pkey":pkey})
cookiejar = r.cookies

if r.status_code != 200:
    with open("error.html", "w") as f:
        f.write(r.text)
    exit()
else:
    print r.text


r = req.post(SERVER + "polls/vote/", data={"poll": 0, "candidate": 1, "value": 1}, cookies=cookiejar)
print r.text
if r.status_code != 200:
    with open("error2.html", "w") as f:
        f.write(r.text)
    exit()


ch = loads(r.text)
ch_params = ch["challenge_params"]
ch_id = ch["challenge"]
params={}
for s in ch_params.split("&"):
    key, val = s.split("=")
    params[key] = val

solution = solve(params["date_pref"], params["salt"], int(params["bits"]))
print solution

r = req.post(SERVER + "polls/vote/", data={"poll": 0, "candidate": 1, "value": 1, 
    "answer": solution, "challenge":ch_id}, cookies=cookiejar)

print r.text.encode("utf-8")
print r.status_code