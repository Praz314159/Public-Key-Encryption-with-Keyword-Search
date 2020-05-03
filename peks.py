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
# import bilinear # cannot import until setup is ready
# import trapdoor_permutation # or whatever Hoa names it

target = None
keywords = []
mode = None

def load_file(filename):
	with open(filename,'r') as f:
		kw_in = f.read().split("\n")
	keywords.extend(kw_in)




"""
 Sample usage: peks <securiy_parameter> <keyword to search> <keywords....>
"""
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-sp","--security-param", choices=["bm","td"],default="bm",
		help="Defines the security parameter used for the trapdoor.")
	parser.add_argument("-t","--test",required=True,
		help="Defines the target keyword to search/test for.")
	parser.add_argument("-k","--keywords",nargs="+",required=False,
		help="Defines the list of encrypted keywords to be tested.")
	parser.add_argument("-kf","--keywords-file", required=False,
		help="Define a new-line separated file to read the encrypted keywords to be tested.")
	args = parser.parse_args()

	mode = args.security_param
	target = args.test
	if args.keywords:
		keywords.extend(args.keywords)
	else:
		if args.keywords_file:
			load_file(args.keywords_file)
		else:
			print("You must specify keywords either via the cli or with an input file (-k/-kf)")
			sys.exit(1)

	# Sanity Check
	print(f"Mode: {mode}")
	print(f"Target: {target}")
	print(f"Keywords: {', '.join(keywords)}")
