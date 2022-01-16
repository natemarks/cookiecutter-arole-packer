Why does this project exist?
I create lots of ansible role projects so having cookiecutter project templates saves me a TONof time when I start new ones.

Why does it test with EC2 instances using packer?
This project is a cookiecutter template for ansible role projects that test the role using packer to spin up EC2 instances. It is a slower, but more flexible alternative to using molecule and docker for testing. It's idea for role sthat need to be tested in complex, multi-user instances like desktop configuration roles. I've never been interested in building out a whole desktop environment in docker, so this project is my solution.

What does it doe for me?
 - setup a minimal project structure
 - use test/secure_vars.yml to provide secure variables. that file is in gitignore by default to minimize the riks of leaking secure data into the repo
 - provide testinfra example
 - scripts for creating and cleaing up a VPC to run packer builds and tests
 - make base-images runs a packer template to create and publish an ubuntu EC2 desktop AMI that the role will be tested on. It can be easily extended.
 - make test runs a packer template to start a supported test instance,  uploads the role and test files, then runes the role and finally the test.
 - make part=[patch|minor|major] bump will bump the role version with tags.


## Prerequisites
You'll need aws credentials configured in your working shell, python and the cookiecutter python package.


## Usage
Assuming you have python installed, this is a safe way to install and use cookiecutter in a virtual environment rather than in your system/user site packages. It assumes that you want to create the ansible role project in $HOME/Projects.
```shell
cd "$(mktemp -d)"
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip setuptools cookiecutter
cd ~/Projects
cookiecutter gh:natemarks/cookiecutter-arole-packer
You've downloaded /Users/nmarks/.cookiecutters/cookiecutter-arole-packer before. Is it okay to delete and re-download it? [yes]:
role_name [my_role]: onguard
github_user [natemarks]:
author [Nate Marks]:
ansible_version [4.10.0]:
galaxy_tag_1 [example_tag1]:
galaxy_tag_2 [example_tag2]:
galaxy_tag_3 [example_tag3]:

deactivate

less arole-onguard/README.md
```

After you create your project the project will have a README.md file in the root that explains how to get started.

Many thanks to our contributor! It wouldn't have occurred to me to use packer for ansible role testing.

[Kyle Hughes](https://github.com/Hugh472)



