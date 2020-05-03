
from pypbc import *
import hashlib
import secrets
import os

class Key:
    def __init__(self, params, priv, pubg, pubh):
        self.params = params
        self.priv = pubg
        self.pubg = pubg
        self.pubh = pubh

    # def store(self, d):
    #     with open(os.path.join(d, 'a.priv'), 'w') as f:
    #         f.write(str(self.priv))
    #     with open(os.path.join(d, 'a.pubg'), 'w') as f:
    #         f.write(str(self.pubg))
    #     with open(os.path.join(d, 'a.pubh'), 'w') as f:
    #         f.write(str(self.pubh))
    #     with open(os.path.join(d, 'a.params'), 'w') as f:
    #         f.write(str(self.params))

    # @classmethod
    # def load(cls, d):
    #     with open(os.path.join(d, 'a.params'), 'r') as f:
    #         pstr = f.read(str(self.params))
    #     with open(os.path.join(d, 'a.priv'), 'r') as f:
    #         privstr = (str(self.priv))
    #     with open(os.path.join(d, 'a.pubg'), 'r') as f:
    #         gstr = f.read(str(self.pubg))
    #     with open(os.path.join(d, 'a.pubh'), 'r') as f:
    #         hstr = f.read(str(self.pubh))

class BilinearMap:
    def __init__(self, keywords):
        self.keywords = keywords

    def genkey(self, s):
        # p = secrets.randbits(s/2)
        # q = secrets.randbits(s/2)
        # n = p*q
        params = Parameters(qbits=512, rbits=160)
        pairing = Pairing(params)
        priv = Element.random(pairing, Zr)
        pubg = Element.random(pairing, G1)
        pubh = pubg ** priv
        self.key = Key(params, priv, pubg, pubh)

    def peks(self, W):
        r = Element.random(self.key.pairing, Zr)
        hr = self.key.pubh ** r
        gr = self.key.pubg ** r

        W_hash = hashlib.sha512(W.encode('utf-8')).digest()
        H1_W = Element.from_hash(self.key.pairing, G1, W_hash)

        t = self.pairing.apply(H1_W, hr)
        # t_hash = hashlib.sha512(
        # H2_t = Element.from_hash(self.key.pairing, G1,
        # return (gr, E

    def trapdoor(self, W):
        W_hash = hashlib.sha512(W.encode('utf-8')).digest()
        H1_W = Element.from_hash(self.key.pairing, G1, W_hash)
        return H1_W ** self.key.priv

    def test(self, ciphertext, trapdoor):
        A, B = ciphertext


