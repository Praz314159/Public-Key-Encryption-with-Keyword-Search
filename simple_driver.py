#!/usr/bin/env python3

from sys import argv
import bilinear

s = int(argv[1])
kw = argv[2]

peks = bilinear.BilinearMap(kw=argv[2:], s=s)
ciphers = [peks.peks(W) for W in argv[3:]]
Tw = peks.trapdoor(kw)

for i, S in enumerate(ciphers):
    if peks.test(S, Tw):
        print("kw is:", argv[i+3])
        exit(1)

print("kw not found")
