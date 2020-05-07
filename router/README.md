
# Router

This suite of programs implements a proof of concept for using the PEKS protocol for dynamically routing mail to a custom destination based on keywords. The gateway is only able to detect the keyword for which it has been supplied a trapdoor. 

## genkey.py

Generates the private and public keys needed for the bilinear map scheme used by PEKS. It also generates a 2048-bit RSA key to encrypt the messages themselves (or more accurately to encrypt the 256-bit AES session key).

Usage: `python3 genkey.py <directory> <qbits> <keywords...>`

The program will produce the following files in the directory supplied:
- params - the parameters defining the bilinear mapping
- priv - the private key value alpha
- pubg/pubg - the public values g and h
- rsa.bin/rsa.pub - the private and public RSA key
- kw - the list of keywords

The private components are only necessary for generating the trapdoors and decrypting the message.

`qbits` is the number of bits in the order the group `G1`.

## encrypt.py

Reads a message from stdin, and produces the encypted message block on stdout. It will produce a publicly searchable encryption for each of the keywords that are found in the message. 

Usage: `python3 encrypt.py <directory>`

The directory supplied contains all the public key elements generated from `genkey.py`.

## mailify.py

This is an optional helper script to be used when testing the program. It reads a message from stdin (useful for piping the output of `encrypt.py` into this script), and produces an email message on its output. This email message can then be passed to `check.py`.


## trapdoor.py

Generates the trapdoors for the keywords supplied. The trapdoors will be placed in the key directory.

Usage: `python3 trapdoor.py <directory> <keywords...>`

For example: `python3 trapdoor.py normal` will produce a file `normal.td` containing the trapdoor for the keyword `normal`. These trapdoors can then be distributed to the necessary gateway servers.

## check.py

Reads an email on stdin, and will produce a modified email on stdout. In particular, the check.py program will change the destination address based on the keyword it has detected. Otherwise, it will set the destination to the default of nokw@dov.ms (no keyword).

## decrypt.py

Decrypts a message block (or email containing a message block) supplied on stdin.

Usage: `python3 decrypt.py <directory>`

## Example usage
Use `scriptreplay` to view a playback of an example usage of this program. To do so, run the following in a terminal: `scriptreplay -t usage.timing usage.script`.


