
import os
import math

from pypbc import *
from Crypto.Hash import SHA3_512

class Key:
    def __init__(self, params, priv, pubg, pubh):
        self.params = params
        self.pairing = Pairing(params)
        self.priv = priv #private key 
        self.pubg = pubg #g's public key
        self.pubh = pubh #h's public key 

        rstr = [l for l in str(params).split('\n') if l.startswith('r')]
        assert(len(rstr) == 1)
        rstr = rstr[0]
        self.p = int(rstr.split(' ')[1])
        self.logp = math.ceil(math.log(self.p, 2))

    def store(self, d):
        if not os.path.exists(d):
            os.mkdir(d)
        def w(f, o):
            with open(os.path.join(d, f), 'w') as fh:
                fh.write(str(o))
        w("params", self.params)
        w("priv", self.priv)
        w("pubg", self.pubg)
        w("pubh", self.pubh)

    @classmethod
    def load(cls, d):
        if not os.path.exists(d):
            raise Exception("no key dir")
        def r(f):
            with open(os.path.join(d, f), 'r') as fh:
                return fh.read()
        params = Parameters(param_string=r("params"))
        pairing = Pairing(params)
        priv = None
        if os.path.exists(os.path.join(d, 'priv')): # optional
            priv = Element(pairing, Zr, value=r("priv"))
        pubg = Element(pairing, G1, value=r("pubg"))
        pubh = Element(pairing, G1, value=r("pubh"))
        return Key(params, priv, pubg, pubh)

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
        h = SHA3_512.new()
        h.update(W.encode('utf-8'))
        W_hash = h.digest()
        H1_W = Element.from_hash(self.key.pairing, G1, W_hash)
        return H1_W

    def H2(self, G2):
        s = str(G2)
        h = SHA3_512.new()
        h.update(s.encode('utf-8'))
        s_hash = h.digest()
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
