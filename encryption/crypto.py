from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from string import ascii_letters
from random import choice


AES_BLOCK_SIZE = 16
SHA_SIZE = 256
AES_PWD_SIZE = 32
RSA_KEY_SIZE = 2048

RSA_HEADER = "-----BEGIN PUBLIC KEY-----\n"
RSA_FOOTER = "\n-----END PUBLIC KEY-----\n"

def sha_hash(content, prefix = None):
    h = SHA256.new()
    if prefix:
        h.update(prefix)
    h.update(content)
    return h.hexdigest()

def aes_derive_key(key):
        k = Cryptography.hash(key + ":key")[0:Cryptography.KEY_SIZE]
        iv = Cryptography.hash(key + ":iv")[0:Cryptography.BLOCK_SIZE]
        return k, iv


def aes_encrypt(content, key):
    # pad
    len_padding = AES_BLOCK_SIZE - (len(content) % AES_BLOCK_SIZE)
    if len_padding == 0: 
        len_padding = AES_BLOCK_SIZE
    padded = content + len_padding * chr(len_padding)
    # encryption
    k, iv = Cryptography.deriveKey(key)
    cipher = AES.new(k, AES.MODE_CBC, iv)
    return cipher.encrypt(padded)


def aes_decrypt(content, key):
    # decryption
    k, iv = Cryptography.deriveKey(key)
    cipher = AES.new(k, AES.MODE_CBC, iv)
    # unpad
    padded = cipher.decrypt(content)
    last = ord(padded[-1])
    return padded[:-last]


def rsa_encrypt(plaintext, key):
    cypher, always_none = key.encrypt(plaintext, "this is ignored")
    return cypher

def rsa_decrypt(ciphertext, key):
    return key.decrypt(ciphertext)



def rsa_recompose(pkey):
    a = []
    n=0
    while n*64 < len(pkey):
        a.append(pkey[n*64:(n+1)*64])
        n+=1

    return "\n".join(a)


def rsa_check(pkey):
    try:
        _ = RSA.importKey(pkey)
    except ValueError:
        try:
            _ = RSA.importKey(RSA_HEADER+pkey+RSA_FOOTER)
        except Exception:
            return False
    return True

def rsa_clean(pkey):
    if pkey.find(RSA_HEADER) == -1:
        return pkey
    else:
        return "\n".join(pkey.split("\n")[1:-1])

def rsa_wrap(pkey):
    if pkey.find(RSA_HEADER) == -1:
        return RSA_HEADER + pkey + RSA_FOOTER
    else:
        return pkey

def generateRSAKeys():
    random_generator = Random.new().read
    key = RSA.generate(RSA_KEY_SIZE, random_generator)
    return key



# def random_int(max):
#     from random import SystemRandom
    
def random_string(l):
    "Return a random string of length 'l'"
    alphabet = ascii_letters + "+/="
    return ''.join([choice(alphabet) for _ in [None]*l])