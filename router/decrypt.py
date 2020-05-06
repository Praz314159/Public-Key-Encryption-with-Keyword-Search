
from sys import argv, stdin
import os.path
import base64

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

def b64(s):
    return base64.b64decode(s.encode('utf-8'))

d = argv[1]
privkey = RSA.import_key(open(os.path.join(d, "rsa.bin")).read())

message = stdin.read()
lines = message.splitlines()

n = 0
while n < len(lines) and not lines[n].startswith("-----BEGIN PEKS"):
    n += 1

enc_sk = b64(lines[n+1])
nonce = b64(lines[n+2])
tag = b64(lines[n+3])
ctxt = b64(lines[n+4])

cipher_rsa = PKCS1_OAEP.new(privkey)
sk = cipher_rsa.decrypt(enc_sk)

cipher_aes = AES.new(sk, AES.MODE_EAX, nonce)
data = cipher_aes.decrypt_and_verify(ctxt, tag)
print(data.decode('utf-8'), end='')
