
from sys import argv, stdin
import os.path
from bilinear import BilinearMap, Key
import base64
import glob
from pypbc import Element, G1
import email
import quopri

def b64(s):
    return base64.b64decode(s.encode('utf-8'))

d = argv[1]

with open(os.path.join(d, "kw")) as fh:
    kw = [line.strip() for line in fh.readlines()]

k = Key.load(d)
bm = BilinearMap(key=k, kw=kw)

# load trapdoors
td = {}
for f in glob.glob(os.path.join(d, "*.td")):
    with open(f, 'r') as fh:
        s = fh.read()
    fname = os.path.basename(f)
    W = os.path.splitext(fname)[0]
    td[W] = Element(bm.key.pairing, G1, value=s)

# parse the email
mail = email.message_from_file(stdin)
if mail.is_multipart():
    for part in mail.get_payload():
        if part.get_content_type() == 'text/plain':
            body = part
else:
    body = mail

pl = body.get_payload()
cte = 'Content-Transfer-Encoding'
if cte in body and body[cte] == 'quoted-printable':
    pl = quopri.decodestring(pl).decode('utf-8')
lines = pl.splitlines()

n = 0
while n < len(lines) and not lines[n].startswith("-----BEGIN PEKS"):
    n += 1

Wx = set()
for i in range(n+5, len(lines), 2):
    if lines[i].startswith("-----END PEKS"):
        break

    gr = Element(bm.key.pairing, G1, value=lines[i])
    H2_t = b64(lines[i+1])
    S = (gr, H2_t)

    for W, Tw in td.items():
        if bm.test(S, Tw):
            Wx.add(W)

del mail['To']

if Wx:
    W = Wx.pop()
    mail['To'] = W + '@dov.ms'
else:
    mail['To'] = 'nokw@dov.ms'

print(mail)
