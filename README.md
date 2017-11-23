# About
Generator of multiplication table tests for Basic School 

# Prerequisites
* Python 3.6

# Installation on Linux or Mac
First install python3 using your favorite package manager.

## Recommendation for Mac users
```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python3
```

## pip install
You can install directly from Github

```bash
pip3 install --upgrade git+https://github.com/jakubzeman/multiplication-table-test-generator.git
```
(In case you need to perform installation for all users (or without virtualenv) then
you will need root permission: `sudo pip install git+https://github.com/jakubzeman/multiplication-table-test-generator.git`)

## Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```bash
python3 setup.py install --user
```
(or `sudo python3 setup.py install` to install the package for all users)

## Installation on MS Windows
First you need to install following packages:
- https://git-scm.com/download
- https://www.python.org/downloads/

Then you need to run from windows cmd shell:
```
pip3 install --upgrade git+https://github.com/jakubzeman/multiplication-table-test-generator.git
```

# Usage
```
Usage: multiplication-test-generator [OPTIONS] COMMAND [ARGS]...

  Examples of usage:

  multiplication-test-generator > test.txt

  multiplication-test-generator --remainder-word 'Zbytek po dělení'

  To change set of small numbers: export SMALL_NUMBER_SET='0 1 2 3 4 5'

  Following command shows version: multiplication-test-generator --version

Options:
  --version                       Show the version and exit.
  --small-number-set <small numbers list>
                                  List of small number from which is random
                                  choice made. Default value is (2, 3, 4, 5,
                                  6, 7, 8, 9).
  --exercise-count <count of exercises>
                                  Maximum count of exercises per type. Default
                                  value is 12
  --remainder-word <remainder value in text>
                                  By default in English. Feel free to rename
                                  it to your language
  -h, --help                      Show this message and exit.
```
