
from pypbc import *
import hashlib
import secrets
import os
import math

class Key:
    def __init__(self, params, priv, pubg, pubh):
        self.params = params
        self.pairing = Pairing(params)
        self.priv = priv
        self.pubg = pubg
        self.pubh = pubh

        rstr = [l for l in str(params).split('\n') if l.startswith('r')]
        assert(len(rstr) == 1)
        rstr = rstr[0]
        self.p = int(rstr.split(' ')[1])
        self.logp = math.ceil(math.log(self.p, 2))

class BilinearMap:
    def __init__(self, kw=[], key=None, s=160):
        self.keywords = kw
        self.key = key or self.genkey(s=s)

    def genkey(self, s=160):
        params = Parameters(qbits=512, rbits=s)
        pairing = Pairing(params)
        priv = Element.random(pairing, Zr)
        pubg = Element.random(pairing, G1)
        pubh = pubg ** priv
        return Key(params, priv, pubg, pubh)

    def H1(self, W):
        W_hash = hashlib.sha512(W.encode('utf-8')).digest()
        H1_W = Element.from_hash(self.key.pairing, G1, W_hash)
        return H1_W

    def H2(self, G2):
        s = str(G2)
        s_hash = hashlib.sha512(s.encode('utf-8')).digest()
        H2_hash = s_hash[:math.ceil(self.key.logp/8)]
        return H2_hash

    def peks(self, W):
        if W not in self.keywords:
            raise Exception("invalid keyword")
        r = Element.random(self.key.pairing, Zr)
        hr = self.key.pubh ** r
        gr = self.key.pubg ** r

        H1_W = self.H1(W)
        t = self.key.pairing.apply(H1_W, hr)
        H2_t = self.H2(t)
        return (gr, H2_t)

    def trapdoor(self, W):
        if W not in self.keywords:
            raise Exception("invalid keyword")
        return self.H1(W) ** self.key.priv

    def test(self, S, Tw):
        A, B = S
        return self.H2(self.key.pairing.apply(Tw, A)) == B
