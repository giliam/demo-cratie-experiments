import requests as req


# creating user

from encryption.crypto import *
from Crypto.PublicKey import RSA


SERVER = "http://localhost:8000/"

password = random_string(20)

key = RSA.generate(1024)
pkey = key.publickey().exportKey()

pkey = "".join(pkey.split("\n")[1:-1])

print "creating user {0} {1}".format(password, pkey)
r = req.post(SERVER + "citizen/create/", data={"password":password, 
    "pkey":pkey})

if r.status_code != 200:
    with open("error.html", "w") as f:
        f.write(r.text)
else:
    print r.text