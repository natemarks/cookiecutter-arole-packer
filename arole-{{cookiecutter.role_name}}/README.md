# natemarks/{{ cookiecutter.role_name }}
Dear Role Developer,

When you create the project these are the things you want to do right away. The goal it to get the 'make test' command running.
 - initialize git
 - create a VPC for test instances
 - build a base AMI with all the requirements, so it's ready to run your role
 - run make test using the base ami

This project was tested with packer 1.7.8. You'll need that or a later version.

NOTE: remember to delete your VPC stack when you don't need it anymore

## initialize git
```shell
git init .
git add -A
git commit -am 'initial'
```

## Create a test VPC
This template assumes you'll want a VPC to build/run your test EC2 instances.  Configure your AWS credentials then run the create script

```shell
export AWS_PROFILE=my-profile
bash scripts/create_test_vpc.sh 
{
    "StackId": "arn:aws:cloudformation:us-east-1:0123456789:stack/test-arole-crowdstrike/4afba790-75f0-11ec-b7f3-0a9cc2eedcb1"
}
Waiting for create-stack to finish
0123456789
vpc-abc123
subnet-abc123
```
This script create the VPC, subnets SSM endpoints and security groups required for SSM. You probably don't need it because packer interacts with the instances using ssh, but it may be convenient to be able to access your instances using session manager.

The script also writes the VPC id, subnet id and account id to the packer vars file (packer/base-test-vars.hcl). This is required to make the next step work seamlessly


## Build a base AMI
The previous step wrote the required variables into packer/base-test-vars.hcl so now you can build the base AMI. 
```shell
make base-images
```


## Run your first test
This command tests the default template role on the base image. It should succeed, but it doesn't do much.
```shell
make test
```

## Delete your VPC stack
```shell
export AWS_PROFILE=my-profile
bash scripts/delete_test_vpc.sh
```


## example playbook for testing
```yaml
---
# example playbook
- hosts: localhost
  become: false
  vars:
    aws_access_key_id: AAAAAAA
    aws_secret_access_key: abc123
    s3_uri: "s3://my_bucket/some/path/to/file"
  roles:
    - /opt/ansible/{{ cookiecutter.role_name }}
```
