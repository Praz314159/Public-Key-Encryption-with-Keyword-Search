# Implementing Public Key Cryptography with Key Word Search

## Prashanth Ramakrishna* Hao Shu† Dov Salomon‡ Jonathan Alter§

## May 5, 2020

## 1 Introduction

For Project 2, we decided to choose Option 6. Option 6 requires summarizing a paper, implementing it’s
constructions, then testing the performance of our implementations as relevant parameters grow. The paper
we chose to implement is entitled, ”Public Key Cryptography with Key Word Search”. This paper attempts
to solve the following question:

Alice is an email user who would like to access her email on multiple devices. However, she would like
emails to be sorted, via routing, to different devices based on certain keywords they contain. For example,
suppose Bob sends Alice an email containing the keyword ”urgent”. This email should be routed to Alice’s
pager rather than her desktop. Such a scheme would be trivial to implement, of course, if Bob’s email were
in plaintext. The gateway, given a set of keywords, could simply search the plaintext and act accordingly.
But, how can such a scheme be accomplished if Bob’s email is encrypted and, along with it, the keywords
contained therein?

In this case, as should be apparent, routing decisions cannot be made by the gateway because keywords are
hidden. This paper develops a scheme whereby Alice enables the gateway to test whether a specified set
of keywords is contained in encrypted emails being received without learning anything else. Formally, Bob
sends Alice an encrypted email of the following form:

```
EApub(M) ||PEKS(Apub,W 1 )|| ...||PEKS(Apub,Wm) (1)
```
whereApubis Alice’s public key,EApubrefers to some standard public key encryption using Alice’s public key,
PEKSis aPublic-Key Encryption with Keyword Searchof each keywordW 1 ,...,Wmsent by Bob in message
M. The advantage of this form is that Alice can provide a trapdoorTW which will allow the gateway to
test whether any of the keywords associated with Bob’s message match Alice’s chosen keywordW. That is,
givenPEKS(Apub,W') andTW, the gateway has the ability to determine ifW=W'. Note that ifW 6 =W',
then the gateway learns nothing further about the email other than thatW6?M.

Definition 1.1.Non-Interactive PEKS [FILL IN DESCRIPTION OF NONINTERACTION PEKS]

```
1.KeyGen(s):KeyGentakes the key length security parametersas input and return a public-private
key pair, denoted{Apub,Apriv}
```
```
2.PEKS(Apub,W): Given public keyApuband wordW,PEKSreturns the searchable encryption ofW.
```
```
3.T(Apriv,W): Alice uses her private keyAprivto create a trapdoorTWfor chosen wordW.
```
```
4.Test(Apub,S,TW): Given Alice’s public key, searchable encryption ofW',S=PEKS(Apub,W'), and
trapdoorTW=T(Apriv,W),Testreturns booleanW=W'.
*pmr347@nyu.edu
†hs3812@nyu.edu
‡dms833@nyu.edu
§ja3943@nyu.edu
```

First, Alice usesKeyGento produce her public/private key pair. Then, she usesTto produce a trapdoor
TWifor eachWi?W*, whereW*is the set of chosen keywords{W 1 ,...,Wm}. This set of trapdoors is
denotedTW*and is given by Alice to her mail server. Alice When Alice’s mail server receives a message
from Bob

```
EApub(M)||S 1 || ...||Sm
```
it usesTestto determine whether message contains any member ofW*.

Security for aPEKSscheme is defined against active attackerAwho, given parameters, is able to query an
oracle for the trapdoorTW of any chosen wordW ? { 0 , 1 }*. Despite this ability,Ashould be unable to
distinguishPEKS(Apub,W 1 ) andPEKS(Apub,W 2 if he hasTW 0 but notTW 1. The challenge for the attacker
is, when given two new keywordsW 0 ,W 1 for which he doesn’t have the trapdoor, and searchable encryption
PEKS(Apub,Wb, whereb?{ 0 , 1 }, to guessb.Awins the security game if his advantage,

```
AdvA(s) =|P(b=b')-
```
### 1

### 2

### | (2)

whereb'isA’s guess, is non-negligible.

Remark 1.1. The general construction given in Def 1.1 is not secure against a chosen cipher text attack,
sinceAcan simply decrypt after reorder the searchable keyword encryptions appended toM. However, Def
1.1 does ensure semantic security for the message form given in Eq 1 so long aEApubis itself semantically
secure. With modifications, chosen cipher-text security can be achieved. Indeed, in the paper, a chosen
ciphertext secure IBE system, IND-ID-CCA, is detailed.

The paper gives two different constructions of the generalPEKSscheme. The first construction is based on a
bilinear function and the second, simpler albeit less efficient one, is based only on general trapdoor permu-
tations. They are detailed in Section 2 and Section 3. In this project, both constructions are implemented

## 2 Bilinear Construction

This construction makes depends on the hardness of a cousin to the Computational Diffie-Hellman problem
known as theBilinear Diffie Hellman Problem.

Definition 2.1.Bilinear Diffie Hellman Problem (BDH)LetG 1 ,G 2 be two groups of fixed prime orderp
with generator setsg 1 andg 2 , respectively. Further, lete:G 1 ×G 1 ?G 2 be a bilinear function. That is,e
satisfies the following properties:

1. Computability:?x 1 ,x 2 ?G 1 ,?polytime algorithmAto computee(x 1 ,x 2 )?G 2
2. Bilinearity:?x 1 ,x 2 ?[1,p] and?g?G 1 ,e(gx^1 ,gx^2 ) =e(g,g)x^1 x^2.
3. Non-degeneracy:?g?g 1 ,e(g,g)?g 2.

Now, fixg?g 1. Giveng,ga,gb,gc?G 1 , computee(g,g)abc ?G 2. If all polytime algorithms have a
negligable advantage in solving BDH, then we say BDH is intractable.

ThePEKSbilinear map construction, in accordance with Def requiresG 1 ,G 2 ,ande. In addition, however,
it requires two hash functionsH 1 :{ 0 , 1 }*?G 1 andH 2 :G 2 ? { 0 , 1 }log(p). The scheme, then consists of
the four functions defined in Def 1.1.

```
1.KeyGen: Security parameterpis the prime order ofG 1 andG 2 .KeyGenrandomly choosesa?Z*p
andg?g 1 .Apub= [g,h=ga] andApriv=a. Finally,{Apub,Apriv}is returned.
```
```
2.PEKS(Apub,W: First,r?Z*pis randomly chosen. Then,t=e(H 1 (W),hr)?G 2 is computed. Finally,
[gr,H 2 (t)] is returned.
```

```
3.T(Apriv,W): given chosen keywordW,Treturned trapdoorTW=H 1 (W)a?G 1.
```
```
4.Test(Apub,S,TW): LetS= [A,B].Testreturns the booleanH 2 (e(TW,A)) =B.
```
The mechanics of the encryption scheme – how and when these functions are used – are inherited from the
generic construction given in Def 1.1. About this scheme, we have our first theorem.

Theorem 1 .The non-interactive searchable encryption scheme (PEKS) with the bilinear map construction
above is semantically secure against a chosen keyword attack in the random oracle model assuming BDH is
intractable.

The proof of Thm 1 is too extensive to include here. The proof’s high level approach, however is not. We
have attack algorithmAwith advantageagainstPEKS.Amakes=qH 2 queries toH 2 and=qTtrapdoor
queries. Further, we have algorithmBthat solves BDH with probability'=eqTqH
2
, whereeis the base of

the natural log. Because, by construction,runtime(A)˜runtime(B), the BDH assumption holding forG 1 ,
'will be negligible, and thus, so will. The proof, therefore, requires the construction ofBsuch that'is
negligible.

## 3 Trapdoor Construction

## 4 Testing

## 5 Conclusion

