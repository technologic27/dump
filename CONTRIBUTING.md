# Contributing to the Threat Intelligence Platform

### Contents

* [Documentation](#documentation)
* [Setting up dev environment](#setting-up-dev-environment)
* [How to store passwords](#How-to-store-passwords)



### Documentation

(Coming soon...)


---

### Setting up dev environment

(These instructions are currently skewed to Mac OS. If you get this working with Linux, please make a PR)

#### Virtual environments

Virtual environments in python are important because you don't want dependencies in this project clashing with another project
(eg when incompatible versions of the same library are needed as a transitive dependency in both projects). 

In addition, virtual environments help in reproducibility. Without virtual environments, your code may run
on your machine, but if it depends on a package that you had used in a previous project, then it will
likely fail when somebody else tries to run your code (or before that, when our continuous integration
server runs your tests).

* `virtualenv` installation: 
```bash
pip3 install virtualenv
```


#### How to store passwords

DO NOT have credentials explicitly written on scripts to be pushed to this repository. Please store personal access keys on your local machine in your root directory, by doing the following: 
```bash
mkdir ~/.company
vim ~/.company/credentials
```
Example of the format of your credentials
```
[cyber4sight]
username = XXX
password = XXX
secret_key = XXX
```
Example of reading credentials
```python
import configparser
import os

config_file_path = os.path.expanduser("~/.copmany/credentials.ini")
config_section_name = "cyber4sight"
config_parser = configparser.ConfigParser()
files_read = config_parser.read(config_file_path)

result = {}
for property, value in config_parser.items('cyber4sight'):
	result[property] = value
```

