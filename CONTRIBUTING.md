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

#### direnv

But virtual environments are usually a pain: you need to remember to activate it with
`source <path-to-venv>/bin/activate` for every new terminal and `deactivate` when you switch projects. 

To smoothen this, we'll use [`direnv`](https://direnv.net/). It's not strictly necessary to install this
(and `direnv` is not available with Windows), but it will make your life much easier once you're developing.
Short description of `direnv`: a way to activate and deactivate virtual environments just by changing directories. 
Eg: when you enter the directory where your repo is, the project's virtual environment is automatically activated.
Within every subdirectory of the repo the virtual environment will still be active, and when you leave the directory
tree of the repo the virtual environment will be automatically deactivated.

* Installation instructions for various flavours of Linux: https://github.com/direnv/direnv#install. For Mac OS,
the easiest is to use [Homebrew]:
```bash
brew install direnv
```

* Post installation setup: https://github.com/direnv/direnv#setup (if you're using bash but not using `~/.bashrc`,
put that line in `~/.bash_profile`)
* To activate this exit your terminal and start a new one.
* Once you do that, you'll get a warning when you're in the repo:
```
direnv: error .envrc is blocked. Run `direnv allow` to approve its content.
```
* Execute that command to use the `.envrc` file:
```bash
direnv allow
```
* If changes to `.envrc` are made in future (eg to use environment variables) then you'll need to `direnv allow` again.

#### pyenv

For next level reproducibility, we should all make sure we're running the same version of python.
[`pyenv`](https://github.com/pyenv/pyenv) provides a way to use multiple versions of python on your system at
the same time. We'll be using `direnv` to tell `pyenv` which version of python to use.

* Installation instructions: https://github.com/pyenv/pyenv#installation
* Install the version of python we'll be using
```bash
pyenv install 3.7.0
```
* Post installation setup - create a directory:
```bash
mkdir -p ~/.config/direnv/
```
* Open or create the file `~/.config/direnv/direnvrc`, and insert:
```
use_python() {
  local python_root=$HOME/.pyenv/versions/$1
  load_prefix "$python_root"
  layout_python "$python_root/bin/python"
}
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

