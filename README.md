# Public-Key-Encryption-with-Keyword-Search
A situation might present itself within which a user would like a system to handle an encrypted message differently 
depending on its content. An obvious, yet undesirable solution to this issue is to grant the system full access to 
the decryption keys in order to properly deal with the message accordingly. A far more desirable option, perhaps, is
to provide the intermediate system with a **trapdoor** which would enable it to search the encrypted message for a specific 
keyword and react accordingly. This would preserve the confidentiality of the message while allowing messages with varying 
keywords to be treated differently.

Email is a common area where this concept can be applied. Suppose Bob is sending an encrypted message to Alice. Alice would
like her mailserver to send messages containing the word 'urgent' to her mobile phone, while messages containing 'lunch' to 
her desktop. Alice can accomplish this, by generating a trapdoor for both 'lunch' and 'urgent' and giving them to the mailserver.
Bob can then use Alice's public key to encrypt each of the keywords in his email and append the results to his email. When the email 
arrives at the server. Alice can instruct the server to handle each situation accordingly when a keyword is detected.

### Conceptual Overview
Components: [PEKS](https://github.com/Praz314159/Public-Key-Encryption-with-Keyword-Search/raw/master/PublicKeyEncryptionwithKeywordSearch.pdf) (*page 3*)

<img src="https://github.com/Praz314159/Public-Key-Encryption-with-Keyword-Search/raw/master/images/components.png" width=600>

Email Structure: [PEKS](https://github.com/Praz314159/Public-Key-Encryption-with-Keyword-Search/raw/master/PublicKeyEncryptionwithKeywordSearch.pdf) (*page 2*)

<img src="https://github.com/Praz314159/Public-Key-Encryption-with-Keyword-Search/raw/master/images/email_peks.png" width=400>

### Prerequisites

There are several prerequisies required to run PEKS. You can install PEKS on your system manually
or use Docker to gather the prerequisites for you.

* Ubuntu 18.04 (lower may work) or WSL
* Python 3.6+
* Pycrptodome (3.9.7)
* Pypbc (0.2)

#### Manual Installation
First, using the terminal, clone this repository and switch into the directory. We have provided a 
convenient script to install some of the unusual requirements of this project.

Then, run:
```
$ sudo ./pbcinstall.sh
```

#### Docker Container

```
# docker run -it dms833/peks /bin/bash
```

This will run a bash shell in a docker container where all the prerequisites have been installed. This repo will be available at `/peks`.


## Running PEKS

The `peks.py` file is the main driver for testing the project. It can be executed from the 
command line, and will output a quick result based on the supplied arguments. It allows users
to test PEKS using either the bilinear matrix or trapdoor construction.

Here is the basic usage.
```
$ ./peks.py --help
usage: peks.py [-h] [-sp SECURITY_PARAM] [-m {bm,td}] -t TEST [--time]
               [-k KEYWORDS [KEYWORDS ...]] [-kf KEYWORDS_FILE] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -sp SECURITY_PARAM, --security-param SECURITY_PARAM
                        Defines the security parameter to be supplied to the
                        constructor. This is mode specific (160 vs. 1024).
  -m {bm,td}, --mode {bm,td}
                        Defines the mode used for the trapdoor. (Bilinear
                        Matrix/ Trapdoor)
  -t TEST, --test TEST  Defines the target keyword to search/test for.
  --time                Print timing statistics
  -k KEYWORDS [KEYWORDS ...], --keywords KEYWORDS [KEYWORDS ...]
                        Defines the list of encrypted keywords to be tested.
  -kf KEYWORDS_FILE, --keywords-file KEYWORDS_FILE
                        Define a new-line separated file to read the encrypted
                        keywords to be tested.
  -d, --debug           Turns on debugging mode.
```

### Sample usage in bilinear matrix mode
```
$ ./peks.py -m bm -t urgent -k lunch dinner urgent important
Keyword found at position 2: urgent
```

### Sample usage in trapdoor mode
```
$ ./peks.py -m td -t urgent -k lunch dinner urgent important
Keyword found at position 2: urgent
```

### Optional specification of a security parameter
Although sensible defaults were supplied for secruity parameter. They may also be supplied as 
commandline arguments.
```
$ ./peks.py -m bm -t urgent -k lunch dinner urgent important -s 512
Keyword found at position 2: urgent
```

### Usage for timing output
Timing data is also available with the `--time` flag. This is useful for
gathering data for graphic representations of mode-specific time variations.
```
$ ./peks.py -m bm -t urgent -k lunch dinner urgent important --time
bm,None,4,0.019075632095336914,0.02433943748474121,0.003979921340942383,0.0029435157775878906

$ ./peks.py -m td -t urgent -k lunch dinner urgent important --time
td,None,4,0.464641809463501,0.0022253990173339844,9.298324584960938e-06,0.002811908721923828
```

## Other Notes:
This project also has a `router` component intended to give a real world example of how
PEKS can be implemented in a mail system. Please see the [router folder](https://github.com/Praz314159/Public-Key-Encryption-with-Keyword-Search/tree/master/router) for more details.

## Built With
* Pycryptodome (https://github.com/Legrandin/pycryptodome)
* Pypbc (https://github.com/debatem1/pypbc)
  * *Some minor fixes needed to be made* (https://github.com/dmsalomon/pypbc)

## Developers
* Jonathan Alter
* Prashanth Ramakrishna
* Dov Salomon
* Hao Shu

## Authors
* *Public Key Encryption with keyword Search* by:
  - **Dan Boneh** 
  - **Giovanni Di Crescenzo** 
  - **Rafail Ostrovsky**
  - **Giuseppe Persianoz**
