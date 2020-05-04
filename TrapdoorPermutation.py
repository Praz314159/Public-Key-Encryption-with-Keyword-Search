from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import csv
from Crypto.Random.random import getrandbits
import random, time, sys


# Please pip3 install pycryptodome

class TrapdoorPermutation:

    def __init__(self, keywords, s=1024, cipher=None):
        '''s is the security parameter, keywords is a list of keywords
        _cipher is optional and holds all the ciphertext S'''
        self.s = s
        self.keywords = keywords
        self._cipher = []

    def __repr__(self):
        cls = type(self)
        return '%s has s = %d' % (cls.__name__, self.s)

    def __setattr__(self, key, value):
        cls = type(self)
        if key == 's':
            if isinstance(value, int):
                self.__dict__[key] = value
            else:
                raise TypeError('%s:%s takes as input an int' % (cls.__name__, key))
        elif key in ['keywords', '_cipher']:
            if isinstance(value, list):
                self.__dict__[key] = value
            else:
                raise TypeError('%s:%s takes as input a keyword list' % (cls.__name__, key))
        elif key == 'keys':
            if isinstance(value, dict):
                self.__dict__[key] = value
            else:
                raise TypeError('%s:%s takes as input a dict of key pairs' % (cls.__name__, key))
        else:
            raise AttributeError

    def keygen(self) -> 'a dict of {keyword:keypair}, and keypairs.txt and keypairs.csv':
        '''This function takes as input a security parameter, G(s) generates a pair of RSA keys.
        Then writes to a file in .'''
        keys_to_file = {}
        keys = {}
        for keyword in self.keywords:
            key = RSA.generate(self.s)
            keys_to_file[keyword] = (key.publickey().export_key(), key.export_key())  # Assuming no replicating keyword
            keys[keyword] = key
            # keys.setdefault(keyword,[]).append(key) Assuming there are multiple repeating keyword

        self.keys = keys
        # writing to a csv file
        with open('keypairs.csv', 'w') as f:
            writer = csv.writer(f)
            for keyword, keypairs in keys_to_file.items():
                writer.writerow([keyword, keypairs])
        # writing to a txt file
        with open('keypairs.txt', 'wb')as f:
            for k, v in keys_to_file.items():
                f.write(k.encode('utf-8') + b'\n')
                f.write(v[0] + b'\n')
                f.write(v[1])
                f.write(b'\n' * 3)

    def peks(self, W=None) -> '(M,E[Pkw, M])':
        '''PEKS takes as input a public key, and a keyword, returns PEKS(A,W)=(M,E[PKw,M])
        PEKS can be called with a keyword, or with no argument'''

        message_length = self.s - 336  # Plaintext length can be at most the length of RSA modulus -2, in bytes.
        # Also 40 bytes are for the hash so in total message length < modulus - 2 - 40 (in bytes)
        if W:
            if W not in self.keywords:
                raise Exception("invalid keyword")
            A_pub = self.keys[W]
            M = getrandbits(message_length)
            M = M.to_bytes(round(message_length / 8), sys.byteorder)
            cipher = PKCS1_OAEP.new(key=A_pub, hashAlgo=None)
            S = cipher.encrypt(M)
            return (M, S)
        else:
            for word in self.keywords:
                M = getrandbits(message_length)
                M = M.to_bytes(round(message_length / 8), sys.byteorder)
                A_pub = self.keys[word]
                cipher = PKCS1_OAEP.new(key=A_pub, hashAlgo=None)
                S = cipher.encrypt(M)
                self._cipher.append(S)
            return self._cipher

    def trapdoor(self, W) -> 'RSA key object':
        '''Takes a keyword, and returns an RSA key object'''
        if W in self.keywords:
            return self.keys[W]
        else:
            raise Exception("invalid keyword")

    def test(self, S, Tw) -> 'Bool 1 or 0':
        '''Returns 1 if a keyword is found, 0 otherwise'''
        cipher = PKCS1_OAEP.new(Tw)
        try:
            M = cipher.decrypt(S[1])
            if not any(byte_xor(M, S[0])):
                return 1
            else:
                return 0
        except:  # If decryption failed and raises exception
            return 0


def byte_xor(b1, b2) -> 'A list of 1 or 0':
    '''Takes as input two byte string, XOR and return a list'''
    return [a ^ b for a, b in zip(b1, b2)]


def test_functionality(s, w):
    '''Test functionality'''
    peks = TrapdoorPermutation(s, w)
    peks.keygen()
    # print(peks.keys)
    # print('*' * 100)
    # print()
    # S = peks.PEKS() if no argument
    ciphers = [peks.PEKS(W) for W in w]
    # for i in ciphers:
    #   print(i)

    # Tw = peks.Trapdoor(w[0])
    # for i, S in enumerate(ciphers):
    # if peks.Test(S, Tw):
    # print("kw is:%s"%w[0])
    Tw = [peks.Trapdoor(word) for word in w]

    for i, S in enumerate(ciphers):
        x = 0
        for tw in Tw:
            if peks.Test(S, tw):
                print("kw %s is decrypted with Tw[%d]" % (w[i], i))
                x += 1
            else:
                print("Tw[%d] cannot decrypt keyword:%s" % (x, w[i]))
                x += 1


def test_time(w):
    '''Test run time'''
    Security_params = [2 ** x for x in range(10, 13)]
    run_time = {}
    for s in Security_params:
        start = time.time()
        test_functionality(s, w)
        end = time.time()
        run_time[s] = round(end - start)
    print(run_time)
    growth_rate = list(run_time.values())
    print("The growth rate as S increases is: ")
    try:
        for index, value in enumerate(growth_rate):
            print(str(((growth_rate[index + 1] - growth_rate[index]) / growth_rate[index]) * 100) + '%')
    except IndexError:
        sys.exit(0)


if __name__ == '__main__':
    s = 1024
    wordlist = ['urgent', 'usual', 'food', 'news', 'super_urgent', 'noturgent', 'topurgent', 'lunch', 'secure', 'jack']
    test_functionality(s, wordlist)
    test_time(wordlist)
