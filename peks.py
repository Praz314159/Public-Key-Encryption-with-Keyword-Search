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

 Python Version: 3.6+

"""
import sys
import argparse
import bilinear
from pprint import pprint
from TrapdoorPermutation import TrapdoorPermutation
from time import time

target = None
keywords = []
mode = None
security_param = None

def dprint(*args):
	if debug:
		print(*args)

def load_file(filename):
	with open(filename,'r') as f:
		kw_in = f.read().split("\n")
	keywords.extend(kw_in)


def process_inputs():
	# Adding target to keywords for initializing Bilinear Map
	input_kw = list(set(keywords) | set((target,)))
	genstart = time()
	if mode == 'bm':
		if security_param:
			peks = bilinear.BilinearMap(kw=input_kw, s=security_param)
		else:
			peks = bilinear.BilinearMap(kw=input_kw)
	elif mode == "td":
		if security_param:
			peks = TrapdoorPermutation(s=security_param, keywords=input_kw)
			peks.keygen()
		else:
			peks = TrapdoorPermutation(keywords=input_kw)
			peks.keygen()
	else:
		raise Exception("Logic Error: unsupported mode [%s]!" % mode)
	genstop = time()

	cipherstart = time()
	ciphers = [peks.peks(W) for W in keywords]
	cipherstop = time()

	trapdoorstart = time()
	Tw = peks.trapdoor(target)
	trapdoorstop = time()

	checkstart = time()
	for i, S in enumerate(ciphers):
		if peks.test(S, Tw) and not args.time:
			print(f"Keyword found at position {i}: {keywords[i]}")
			return
	checkstop =  time()

	if not args.time:
		print("No keyword found!")
	else:
		gentime = genstop - genstart
		ciphertime = cipherstop - cipherstart
		trapdoortime = trapdoorstop - trapdoorstart
		checktime = checkstop - checkstart
		print(mode, security_param, len(input_kw), gentime, ciphertime, trapdoortime, checktime, sep=',')

"""
 Sample usage: peks <securiy_parameter> <keyword to search> <keywords....>
"""
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-sp","--security-param",type=int, required=False, 
		help="Defines the security parameter to be supplied to the constructor. This is mode specific (160 vs. 1024).")
	parser.add_argument("-m","--mode", choices=["bm","td"],default="bm",
		help="Defines the mode used for the trapdoor. (Bilinear Matrix/ Trapdoor)")
	parser.add_argument("-t","--test",required=True,
		help="Defines the target keyword to search/test for.")
	parser.add_argument("--time",required=False, action='store_true',
		help="Print timing statistics")
	parser.add_argument("-k","--keywords",nargs="+",required=False,
		help="Defines the list of encrypted keywords to be tested.")
	parser.add_argument("-kf","--keywords-file", required=False,
		help="Define a new-line separated file to read the encrypted keywords to be tested.")
	parser.add_argument("-d","--debug",action="store_true",default=False, help="Turns on debugging mode.")
	args = parser.parse_args()

	debug = args.debug

	dprint(args)
	security_param = args.security_param
	mode = args.mode
	target = args.test
	if args.keywords:
		keywords.extend(args.keywords)
		# Does target need to be in keywords???
	else:
		if args.keywords_file:
			load_file(args.keywords_file)
		else:
			print("You must specify keywords either via the cli or with an input file (-k/-kf)")
			sys.exit(1)

	# Sanity Check
	dprint(f"Mode: {mode}")
	dprint(f"Security-Parameter: {security_param}")
	dprint(f"Target: {target}")
	dprint(f"Keywords: {', '.join(keywords)}")

	process_inputs()
