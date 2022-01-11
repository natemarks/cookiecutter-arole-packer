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


```shell
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

cd arole-onguard  
```

```shell
git init .
git add -A
git commit -am 'initial'


```

Create the pythogn virtual environment. If you don't plan to use bump2version or anyo the pytest mpodules locally you can skip this
```shell
make clean-venv

```

Configure the AWS credentials
```shell
export AWS_PROFILE=my_profile
# alternatively export the ID and KEY
```


To use packer for role testing you need an instance which requires a VPC. scripts/create_test_vpc.sh  creates a VPC with some common config that I like. scripts/delete_test_vpc.sh can be used to destroy the VPC when you're done.  the creat script alsp echoes the VPC/subnet and ami owner data into packer/base-test-vars.hcl. This is required to launche instances
```shell
bash scripts/create_test_vpc.sh
{
"StackId": "arn:aws:cloudformation:us-east-1:709310380790:stack/test-arole-onguard/d65684b0-72c9-11ec-aea4-0ea66c843b01"
}
Waiting for create-stack to finish
709310380790
vpc-0eae090a66a10e334
subnet-014772f50235a3264
```


In order to test a role, you need a representative base image. In this example, the role requries ubuntu 20.04 with the gnome desktop packages installed, so we create that base AMI using packer and the VPC we just created.

```shell
make base-images
cp -R defaults packer/upload; cp -R files packer/upload; cp -R handlers packer/upload; cp -R meta packer/upload; cp -R playbook packer/upload; cp -R tasks packer/upload; cp -R templates packer/upload; cp -R test packer/upload;
( \
. ./.env && cd packer && packer build \
-var-file="base-test-vars.hcl" base-test-images.pkr.hcl; \
)
Warning: Undefined variable

A "ami_owner" variable was set but was not found in known variables. To declare
variable "ami_owner", place this block in one of your .pkr files, such as
variables.pkr.hcl


ansible-test-arole-onguard.amazon-ebs.ubuntu: output will be in this color.

==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Force Deregister flag found, skipping prevalidating AMI Name
ansible-test-arole-onguard.amazon-ebs.ubuntu: Found Image ID: ami-0d4c664d2c7345cf1
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Creating temporary keypair: packer_61dd5f3e-78b3-5027-86e2-e052a3fb51ce
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Creating temporary security group for this instance: packer_61dd5f40-db4c-486f-3ddd-b5e56b4894a3
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Authorizing access to port 22 from [0.0.0.0/0] in the temporary security groups...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Launching a source AWS instance...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Adding tags to source instance
ansible-test-arole-onguard.amazon-ebs.ubuntu: Adding tag: "Name": "Packer Builder"
ansible-test-arole-onguard.amazon-ebs.ubuntu: Instance ID: i-0840c06ce133de449
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Waiting for instance (i-0840c06ce133de449) to become ready...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Using SSH communicator to connect: 3.238.220.204
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Waiting for SSH to become available...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Connected to SSH!
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Uploading ./scripts => /tmp/
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Uploading ./files => /tmp/
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Provisioning with shell script: /var/folders/72/cmp8x83n3js_spr_3hvvdgch0000gn/T/packer-shell124179649
==> ansible-test-arole-onguard.amazon-ebs.ubuntu:
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
==> ansible-test-arole-onguard.amazon-ebs.ubuntu:
ansible-test-arole-onguard.amazon-ebs.ubuntu: Get:1 http://security.ubuntu.com/ubuntu focal-security InRelease [114 kB]
ansible-test-arole-onguard.amazon-ebs.ubuntu: Hit:2 http://archive.ubuntu.com/ubuntu focal InRelease
ansible-test-arole-onguard.amazon-ebs.ubuntu: Get:3 http://archive.ubuntu.com/ubuntu focal-updates InRelease [114 kB]
ansible-test-arole-onguard.amazon-ebs.ubuntu: Get:4 http://security.ubuntu.com/ubuntu focal-security/main amd64 Packages [1128 kB]
...  # Install a trillion packages for ubuntu desktop
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: sudo python3 -m site
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: + sudo python3 -m site
ansible-test-arole-onguard.amazon-ebs.ubuntu: sys.path = [
ansible-test-arole-onguard.amazon-ebs.ubuntu:     '/home/ubuntu',
ansible-test-arole-onguard.amazon-ebs.ubuntu:     '/usr/lib/python38.zip',
ansible-test-arole-onguard.amazon-ebs.ubuntu:     '/usr/lib/python3.8',
ansible-test-arole-onguard.amazon-ebs.ubuntu:     '/usr/lib/python3.8/lib-dynload',
ansible-test-arole-onguard.amazon-ebs.ubuntu:     '/usr/local/lib/python3.8/dist-packages',
ansible-test-arole-onguard.amazon-ebs.ubuntu:     '/usr/lib/python3/dist-packages',
ansible-test-arole-onguard.amazon-ebs.ubuntu: ]
ansible-test-arole-onguard.amazon-ebs.ubuntu: USER_BASE: '/root/.local' (doesn't exist)
ansible-test-arole-onguard.amazon-ebs.ubuntu: USER_SITE: '/root/.local/lib/python3.8/site-packages' (doesn't exist)
ansible-test-arole-onguard.amazon-ebs.ubuntu: ENABLE_USER_SITE: True
==> ansible-test-arole-onguard.amazon-ebs.ubuntu:
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: # configure ansible to us the hosts (localhost) paths that the pacaker provisioner wants to use
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: # ansible-playbook ansible/build_azure_agent_ami.yml should work the same way the provisioner does
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: # ths is important for troubleshooting
==> ansible-test-arole-onguard.amazon-ebs.ubuntu:
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: # backup the default config files
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: sudo cp /etc/ansible/hosts /etc/ansible/hosts.orig || true
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: + sudo cp /etc/ansible/hosts /etc/ansible/hosts.orig
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: cp: cannot stat '/etc/ansible/hosts': No such file or directory
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: + true
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: sudo cp /etc/ansible/ansible.cfg /etc/ansible/ansible.cfg.orig || true
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: + sudo cp /etc/ansible/ansible.cfg /etc/ansible/ansible.cfg.orig
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: cp: cannot stat '/etc/ansible/ansible.cfg': No such file or directory
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: + true
==> ansible-test-arole-onguard.amazon-ebs.ubuntu:
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: # set the roles directory to match the provisioning staging dir: /ansible/roles
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: # set the default transport to local
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: sudo mkdir -p /etc/ansible
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: + sudo mkdir -p /etc/ansible
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: sudo cp /tmp/files/install_ansible_prereqs/al2/etc/ansible/ansible.cfg /etc/ansible
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: + sudo cp /tmp/files/install_ansible_prereqs/al2/etc/ansible/ansible.cfg /etc/ansible
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: sudo chmod 644 /etc/ansible/ansible.cfg
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: + sudo chmod 644 /etc/ansible/ansible.cfg
==> ansible-test-arole-onguard.amazon-ebs.ubuntu:
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: # define a single host named 'localhost' wth the value 127.0.0.1
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: sudo cp /tmp/files/install_ansible_prereqs/al2/etc/ansible/hosts /etc/ansible
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: + sudo cp /tmp/files/install_ansible_prereqs/al2/etc/ansible/hosts /etc/ansible
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: sudo chmod 644 /etc/ansible/hosts
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: + sudo chmod 644 /etc/ansible/hosts
==> ansible-test-arole-onguard.amazon-ebs.ubuntu:
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: sudo chown -R root:root /etc/ansible
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: + sudo chown -R root:root /etc/ansible
==> ansible-test-arole-onguard.amazon-ebs.ubuntu:
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: # the provisioner will ise this path to upload the roles. create it and grant the permissions
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: # the provisioner will use
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: sudo mkdir /ansible
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: + sudo mkdir /ansible
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: sudo chown -R ubuntu:root /ansible
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: + sudo chown -R ubuntu:root /ansible
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Provisioning with shell script: /var/folders/72/cmp8x83n3js_spr_3hvvdgch0000gn/T/packer-shell1808823948
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Stopping the source instance...
ansible-test-arole-onguard.amazon-ebs.ubuntu: Stopping instance
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Waiting for the instance to stop...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Creating AMI ansible-test-arole-onguard-ubuntu from instance i-0840c06ce133de449
ansible-test-arole-onguard.amazon-ebs.ubuntu: AMI: ami-09cfe4e98f6ca4d2b
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Waiting for AMI to become ready...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Skipping Enable AMI deprecation...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Terminating the source AWS instance...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Cleaning up any extra volumes...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: No volumes to clean up, skipping
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Deleting temporary security group...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Deleting temporary keypair...
Build 'ansible-test-arole-onguard.amazon-ebs.ubuntu' finished after 17 minutes 44 seconds.

==> Wait completed after 17 minutes 44 seconds

==> Builds finished. The artifacts of successful builds are:
--> ansible-test-arole-onguard.amazon-ebs.ubuntu: AMIs were created:
us-east-1: ami-09cfe4e98f6ca4d2b
```


Now the base image exists we can use packer to test the example role. The tempalte just includes  some logic to install and test makemine as a simple example
```shell
make test
cp -R defaults packer/upload; cp -R files packer/upload; cp -R handlers packer/upload; cp -R meta packer/upload; cp -R playbook packer/upload; cp -R tasks packer/upload; cp -R templates packer/upload; cp -R test packer/upload;
( \
. ./.env && cd packer && packer build \
-var-file="base-test-vars.hcl" run-tests.pkr.hcl; \
)
ansible-test-arole-onguard.amazon-ebs.ubuntu: output will be in this color.

==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Prevalidating any provided VPC information
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Prevalidating AMI Name: run-ansible-test-arole-onguard-ubuntu
ansible-test-arole-onguard.amazon-ebs.ubuntu: Found Image ID: ami-09cfe4e98f6ca4d2b
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Creating temporary keypair: packer_61dd652c-ffd6-ba88-ffd7-12a319a66b90
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Creating temporary security group for this instance: packer_61dd652f-2310-9018-f26c-d23ab9ccdb04
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Authorizing access to port 22 from [0.0.0.0/0] in the temporary security groups...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Launching a source AWS instance...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Adding tags to source instance
ansible-test-arole-onguard.amazon-ebs.ubuntu: Adding tag: "Name": "Packer Builder"
ansible-test-arole-onguard.amazon-ebs.ubuntu: Instance ID: i-04eace3e98e723578
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Waiting for instance (i-04eace3e98e723578) to become ready...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Using SSH communicator to connect: 34.201.21.122
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Waiting for SSH to become available...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Connected to SSH!
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Uploading ./upload => /tmp/
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Provisioning with shell script: /var/folders/72/cmp8x83n3js_spr_3hvvdgch0000gn/T/packer-shell2816776066
ansible-test-arole-onguard.amazon-ebs.ubuntu: defaults
ansible-test-arole-onguard.amazon-ebs.ubuntu: files
ansible-test-arole-onguard.amazon-ebs.ubuntu: handlers
ansible-test-arole-onguard.amazon-ebs.ubuntu: meta
ansible-test-arole-onguard.amazon-ebs.ubuntu: playbook
ansible-test-arole-onguard.amazon-ebs.ubuntu: tasks
ansible-test-arole-onguard.amazon-ebs.ubuntu: templates
ansible-test-arole-onguard.amazon-ebs.ubuntu: test
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Provisioning with shell script: /var/folders/72/cmp8x83n3js_spr_3hvvdgch0000gn/T/packer-shell554111814
ansible-test-arole-onguard.amazon-ebs.ubuntu:
ansible-test-arole-onguard.amazon-ebs.ubuntu: PLAY [localhost] ***************************************************************
ansible-test-arole-onguard.amazon-ebs.ubuntu:
ansible-test-arole-onguard.amazon-ebs.ubuntu: TASK [Gathering Facts] *********************************************************
ansible-test-arole-onguard.amazon-ebs.ubuntu: ok: [127.0.0.1]
ansible-test-arole-onguard.amazon-ebs.ubuntu:
ansible-test-arole-onguard.amazon-ebs.ubuntu: TASK [/opt/ansible/onguard : Download makemine tarball] ************************
ansible-test-arole-onguard.amazon-ebs.ubuntu: changed: [127.0.0.1]
ansible-test-arole-onguard.amazon-ebs.ubuntu:
ansible-test-arole-onguard.amazon-ebs.ubuntu: TASK [/opt/ansible/onguard : Extract /tmp/makemine_0.0.5_linux_amd64.tar.gz in /tmp] ***
ansible-test-arole-onguard.amazon-ebs.ubuntu: changed: [127.0.0.1]
ansible-test-arole-onguard.amazon-ebs.ubuntu:
ansible-test-arole-onguard.amazon-ebs.ubuntu: TASK [/opt/ansible/onguard : Copy makemine to /usr/local/bin] ******************
ansible-test-arole-onguard.amazon-ebs.ubuntu: changed: [127.0.0.1]
ansible-test-arole-onguard.amazon-ebs.ubuntu:
ansible-test-arole-onguard.amazon-ebs.ubuntu: PLAY RECAP *********************************************************************
ansible-test-arole-onguard.amazon-ebs.ubuntu: 127.0.0.1                  : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ansible-test-arole-onguard.amazon-ebs.ubuntu:
ansible-test-arole-onguard.amazon-ebs.ubuntu: ============================= test session starts ==============================
ansible-test-arole-onguard.amazon-ebs.ubuntu: platform linux -- Python 3.8.10, pytest-6.2.5, py-1.11.0, pluggy-1.0.0 -- /usr/bin/python3
ansible-test-arole-onguard.amazon-ebs.ubuntu: cachedir: .pytest_cache
ansible-test-arole-onguard.amazon-ebs.ubuntu: rootdir: /opt/ansible/onguard/test
ansible-test-arole-onguard.amazon-ebs.ubuntu: plugins: testinfra-6.5.0
ansible-test-arole-onguard.amazon-ebs.ubuntu: collecting ... collected 6 items
ansible-test-arole-onguard.amazon-ebs.ubuntu:
ansible-test-arole-onguard.amazon-ebs.ubuntu: ../../opt/ansible/onguard/test/test_infra.py::test_run_binaries[local-wget --version-0] PASSED [ 16%]
ansible-test-arole-onguard.amazon-ebs.ubuntu: ../../opt/ansible/onguard/test/test_infra.py::test_run_binaries[local-curl --version-0] PASSED [ 33%]
ansible-test-arole-onguard.amazon-ebs.ubuntu: ../../opt/ansible/onguard/test/test_infra.py::test_run_binaries[local-python3 --version-0] PASSED [ 50%]
ansible-test-arole-onguard.amazon-ebs.ubuntu: ../../opt/ansible/onguard/test/test_infra.py::test_run_binaries[local-ansible --version-0] PASSED [ 66%]
ansible-test-arole-onguard.amazon-ebs.ubuntu: ../../opt/ansible/onguard/test/test_infra.py::test_run_binaries[local-makemine https:/gist.githubusercontent.com/natemarks/3620f565dc4e775143647d62c151658e/raw/54559a95b3ba58c0cc2ca8889ea12c72adbf7adb/makemine.json-0] PASSED [ 83%]
ansible-test-arole-onguard.amazon-ebs.ubuntu: ../../opt/ansible/onguard/test/test_infra.py::test_makemine[local] PASSED [100%]
ansible-test-arole-onguard.amazon-ebs.ubuntu:
ansible-test-arole-onguard.amazon-ebs.ubuntu: ============================== 6 passed in 0.88s ===============================
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Stopping the source instance...
ansible-test-arole-onguard.amazon-ebs.ubuntu: Stopping instance
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Waiting for the instance to stop...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Skipping AMI creation...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Skipping Enable AMI deprecation...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Skipping AMI region copy...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Skipping AMI modify attributes...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Skipping AMI create tags...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Terminating the source AWS instance...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Cleaning up any extra volumes...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: No volumes to clean up, skipping
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Deleting temporary security group...
==> ansible-test-arole-onguard.amazon-ebs.ubuntu: Deleting temporary keypair...
Build 'ansible-test-arole-onguard.amazon-ebs.ubuntu' finished after 2 minutes 28 seconds.

==> Wait completed after 2 minutes 28 seconds

==> Builds finished but no artifacts were created.
```


Many thanks to our contributor! It wouldn't have occurred to me to use packer for ansible role testing.

[Kyle Hughes](https://github.com/Hugh472)



