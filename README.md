Cookiecutter template for ansible role projects

 - Setup a minimal project structure
 - get molecule linting and test working immediately
 - use .env to provide secure variables to test runs without leaking into the repo
 - provide testinfra example
 - provide a Makefile that useful locally and in pipelines


## Usage
If you don't want to install cookiecutter system wide, just install it in a .venv
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip setuptools cookiecutter
cookiecutter gh:natemarks/cookiecutter-ansible-role
❯ cookiecutter gh:natemarks/cookiecutter-ansible-role
You've downloaded /Users/nmarks/.cookiecutters/cookiecutter-ansible-role before. Is it okay to delete and re-download it? [yes]:
role_name [my_role]: ttt
github_user [natemarks]:
author [Nate Marks]:
ansible_version [4.4.0]:
molecule_version [3.4.0]:
ansible_lint_version [5.1.2]:
galaxy_tag_1 [example_tag1]:
galaxy_tag_2 [example_tag2]:
galaxy_tag_3 [example_tag3]:
vpc_id [vpc-xxx]: vpc-07c33af8d72120e2f
subnet_id [subnet-xxx]: subnet-004abac234ef4680f
ami_id [ami-xxx]: ami-01f64789ff539c77a
❯ cd arole-ttt
❯ make clean-venv

# export AWS configuration environment variables
# AWS_ACCESS_KEY_ID=...
# AWS_SECRET_ACCESS_KEY=...
# NOTE: molecule-ec2 will fail if you use an AWS account that does not have a default VPC
# https://github.com/ansible-community/molecule-ec2/issues/56

# initialize your git repo
git init .
git add -A
git commit -am 'initial'

# these should run successfully
make clean-venv && make molecule-test
```

## Contributors

Many thanks to our contributor!

[Kyle Hughes](https://github.com/Hugh472)

