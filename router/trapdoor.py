
from sys import argv, stdin
import os.path
from bilinear import BilinearMap, Key
import base64

d = argv[1]

with open(os.path.join(d, "kw")) as fh:
    kw = [line.strip() for line in fh.readlines()]

key = Key.load(d)
bm = BilinearMap(key=key, kw=kw)

for W in argv[2:]:
    try:
        s = str(bm.trapdoor(W))
        with open(os.path.join(d, W + ".td"), "w") as fh:
            fh.write(s)
    except Exception as e:
        print(e)
