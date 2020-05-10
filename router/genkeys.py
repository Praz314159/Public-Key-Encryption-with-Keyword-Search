
from sys import argv
import os.path
from bilinear import BilinearMap

from Crypto.PublicKey import RSA

d = argv[1]
qbits = int(argv[2])

bm = BilinearMap(kw=argv[3:], s=qbits)
bm.key.store(d)

with open(os.path.join(d, "kw"), 'w') as fh:
    fh.writelines(k+'\n' for k in argv[3:])

asym = RSA.generate(2048)
with open(os.path.join(d, "rsa.bin"), 'wb') as fh:
    fh.write(asym.export_key())
with open(os.path.join(d, "rsa.pub"), 'wb') as fh:
    fh.write(asym.publickey().export_key())
