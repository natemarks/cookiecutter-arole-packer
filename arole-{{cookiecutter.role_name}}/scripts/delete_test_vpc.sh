#!/usr/bin/env bash
aws cloudformation delete-stack --stack-name "test-arole-{{ cookiecutter.role_name }}"

echo "Waiting for delete-stack to finish"
aws cloudformation wait stack-delete-complete --stack-name "test-arole-{{ cookiecutter.role_name }}"

echo "Stack deleted: test-arole-{{ cookiecutter.role_name }}"