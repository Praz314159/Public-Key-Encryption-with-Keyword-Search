# Public-Key-Encryption-with-Keyword-Search
A situation might present itself within which a user would like a system to handle an encrypted message differently 
depending on its content. An obvious, yet undesirable solution to this issue is to grant the system full access to 
the decryption keys in order to properly deal with the message accordingly. A far more desirable option, perhaps, is
to provide the intermediate system with a trapdoor which would enable it to search the encrypted message for a specific 
keyword and react accordingly. This would preserve the confidentiality of the message while allowing messages with varying 
keywords to be treated differently.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

There are several prerequisies required to run PEKS. You can install PEKS on your system manually
or use Docker to gather the prerequisites for you.

* Ubuntu 18.04 (lower may work) or WSL

#### Manual Installation



```
Give examples
```

#### Docker Installing

Some text explaining.

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

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

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
