#!/usr/bin/env bash
aws cloudformation create-stack --stack-name "test-arole-{{ cookiecutter.role_name }}" \
--template-url  "https://natemarks-cloudformation-public.s3.amazonaws.com/cfn-vpc/vpc.json" \
--tags Key=deleteme,Value=true Key=deleteme_after,Value=2022-01-08
echo "Waiting for create-stack to finish"
aws cloudformation wait stack-create-complete --stack-name "test-arole-{{ cookiecutter.role_name }}"

SUBNET_ID="$(aws cloudformation describe-stacks --stack-name "test-arole-{{ cookiecutter.role_name }}" --output text | grep 'SubnetPublic0' | awk '{print $9}')"
VPC_ID="$(aws cloudformation describe-stacks --stack-name "test-arole-{{ cookiecutter.role_name }}" --output text | grep 'VPCID' | awk '{print $6}')"
AMI_OWNER="$(aws sts get-caller-identity --output text | awk '{print $1}')"

echo "vpc_id = \"${VPC_ID}\"" >> packer/base-test-vars.hcl
echo "subnet_id = \"${SUBNET_ID}\"" >> packer/base-test-vars.hcl
echo "ami_owner = \"${AMI_OWNER}\"" >> packer/base-test-vars.hcl

echo "${VPC_ID}"
echo "${SUBNET_ID}"
echo "${AMI_OWNER}"
