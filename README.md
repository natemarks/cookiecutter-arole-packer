Cookiecutter template for ansible role projects that use packer and AWS EC2 instances to test the roles. This is ideal for cases where docker won't work.

 - Setup a minimal project structure
 - use .env to provide secure variables to test runs without leaking into the repo
 - provide testinfra example
 - provide a Makefile that useful locally and in pipelines
 - make command to create and publish base AMI images. the role is tested by running it on these base images
 - make commands for testing that run locally AND in pipelines
 - make commands for version bumping


## Prerequisites
You'll need aws credentials configured in your working shell.  You can specify an existing VPC and public subnet for testing in the .env file OR you can use scripts/create_test_vpc.sh and scripts/delete_test_vpc.sh to create and cleanup a test VPC.

## Usage

run cookiecutter and specify this project to create a local ansible role project from this cookiecutter template
If you don't want to install cookiecutter system wide, just install it in a .venv
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip setuptools cookiecutter
cookiecutter gh:natemarks/cookiecutter-arole-packer
```

### Optional: Create a test VPC and subnet
If you don't already have a VPC adn public subnet that  you want to use just run the commands below.

NOTE: Like all of my automation the script that turns up the resources tags the stack deleteme:true so it's easy to clean up externally
```shell
# create the stack
bash scripts/create_test_vpc.sh
{
    "StackId": "arn:aws:cloudformation:us-east-1:371143864265:stack/test-arole-ggg/77075e80-6fb8-11ec-b307-0e7d8aa00eff"
}
Waiting for create-stack to finish
subnet-0f1cde6d823dca648
vpc-0f09fcd34b77e182e

# delete the stack
bash scripts/delete_test_vpc.sh
Waiting for delete-stack to finish
Stack deleted: test-arole-ggg
```
Edit the project .env file. Add the vpc ID and subnet ID to use for testing

### Create a test AWS EC2 AMI image in your AWS account
In order to use packer to test the roles, you need to create the project test image(s) in your AWS account.  The default template creates a single ubuntu desktop image as an example. Your project may need one or more different images to test your role under a number of platforms/initial circumstances.

TO create the AMI and publish it to your AWS account, open a shell in your ansible project directory.  Set your AWS credentials and run:
```
make base-images
```
The default image name is in the format. It will overrwite so the name is always the same
ansible-test-arole-[ROLE_NAME]

Many thanks to our contributor! It wouldn't have occurred to me to use packer for ansible role testing.

[Kyle Hughes](https://github.com/Hugh472)

