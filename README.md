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

run cookiecutter and specify this project to create a local ansible role project from this cookiecutter template
If you don't want to install cookiecutter system wide, just install it in a .venv
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip setuptools cookiecutter
cookiecutter gh:natemarks/cookiecutter-arole-packer
```

### Create a test AWS EC2 AMI image in your AWS account
In order to use packer to test the roles, you need to create the project test image(s) in your AWS account.  The default template creates a single ubuntu desktop image as an example. Your project may need one or more different images to test your role under a number of platforms/initial circumstances.

TO create the AMI and publish it to your AWS account, open a shell in your ansible project directory.  Set your AWS credentials and run:
```
make packer-publish
```
The default image name is in the format:
ansible-test-arole-[ROLE_NAME]-[EPOCH_TIME] 

Many thanks to our contributor! It wouldn't have occurred to me to use packer for ansible role testing.

[Kyle Hughes](https://github.com/Hugh472)

