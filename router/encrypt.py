
from sys import argv, stdin
import os.path
from bilinear import BilinearMap, Key
import base64

def b64(b):
    return base64.b64encode(b).decode('utf-8')

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

d = argv[1]

with open(os.path.join(d, "kw")) as fh:
    kw = [line.strip() for line in fh.readlines()]

message = stdin.read()

# encrypt the message
pk = RSA.import_key(open(os.path.join(d, "rsa.pub")).read())
sk = get_random_bytes(32)

cipher_rsa = PKCS1_OAEP.new(pk)
enc_sk = cipher_rsa.encrypt(sk)

cipher_aes = AES.new(sk, AES.MODE_EAX)
ctxt, tag = cipher_aes.encrypt_and_digest(message.encode('utf-8'))
cnonce = cipher_aes.nonce

k = Key.load(d)
bm = BilinearMap(key=k, kw=kw)

keywords = set(W for W in message.split() if W in kw)
peks = [bm.peks(W) for W in keywords]

print("-----BEGIN PEKS MESSAGE-----")
print(b64(enc_sk))
print(b64(cipher_aes.nonce))
print(b64(tag))
print(b64(ctxt))
for p in peks:
    print(p[0])
    print(b64(p[1]))
print("-----END PEKS MESSAGE-----")
