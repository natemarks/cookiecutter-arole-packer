Cookiecutter template for ansible role projects that use packer and AWS EC2 instances to test the roles. This is ideal for cases where docker won't work.

 - Setup a minimal project structure
 - use .env to provide secure variables to test runs without leaking into the repo
 - provide testinfra example
 - provide a Makefile that useful locally and in pipelines
 - make command to create and publish the role test AMI to your AWS account
 - make commands for testing that run locally AND in pipelines
 - make commands for version bumping
 - future: make commands to spin up an asg with a few test instances to shorten test cycles


## Usage
If you don't want to install cookiecutter system wide, just install it in a .venv
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip setuptools cookiecutter
cookiecutter gh:natemarks/cookiecutter-arole-packer
```

## Contributors

Many thanks to our contributor! It wouldn't have occurred to me to use packer for ansible role testing.

[Kyle Hughes](https://github.com/Hugh472)

