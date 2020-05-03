#! /usr/bin/python3
"""
 The following program is intended to demonstrate the concept of
 Public Key Encryption with Keyword Search*.

 Brief Summary:
 We have implemented two different constructions to generate
 trapdoors for possible keywords. These constructions are outlined
 in the aformentioned paper. The first contruction uses bilinear
 maps and the second utilizes trapdoor permutations.

 * - Based on the paper by Dan Boneh, Giovanni Di Crescenzo, Rafail
     Ostrovsky, and Guiseppe Persiano
"""
import argparse
import bilinear
# import trapdoor_permutation # or whatever Hoa names it

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argment("-bm")

	s = int(sys.argv[1])
	kw = sys.argv[2]

	peks = bilinear.BilinearMap(kw=sys.argv[3:], s=s)
	ciphers = [peks.peks(W) for W in sys.argv[3:]]
	Tw = peks.trapdoor(kw)

	for i, S in enumerate(ciphers):
		if peks.test(S, Tw):
			print("kw is:", sys.argv[i+3])
			exit(1)

	print("kw not found")

