"""Test variou executions of the cookiecutter
Each parametrize test case is a set of cookiecutter json overrides

"""
import logging
import os
import pytest
import testinfra  # pylint: disable=W0611
from cookiecutter.main import cookiecutter

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

PROJECT_DIR = os.getcwd()


@pytest.mark.parametrize(
    "ccinput",
    [
        (
            {
                "role_name": "fff",
                "vpc_id": "vpc-fff",
                "subnet_id": "subnet-fff",
                "ami_id": "ami-fff"
            }),
        (
            {
                "role_name": "ggg",
                "vpc_id": "vpc-ggg",
                "subnet_id": "subnet-ggg",
                "ami_id": "ami-ggg"
            }),
    ],
)
class TestClass:  # pylint: disable=R0903
    """Table test the cookiecutter options"""

    def test_(
        self, host, tmp_path, ccinput
    ):  # pylint: disable=R0201
        """Iterate on different cookiecutter json overrides"""
        role_dir=str(tmp_path) + "/" + "arole-" + ccinput["role_name"]
        os.chdir(tmp_path)
        log.info("tmpdir: %s", str(tmp_path))
        cookiecutter(
            PROJECT_DIR,
            no_input=True,
            extra_context=ccinput,
        )
        #  check env file
        env_file = host.file(role_dir + '/.env')
        assert env_file.exists
        assert env_file.contains('^export VPC_ID='+str(ccinput["vpc_id"]))
        assert env_file.contains('^export SUBNET_ID='+str(ccinput["subnet_id"]))
        assert env_file.contains('^export AMI_ID='+str(ccinput["ami_id"]))
        # check packer base template
        packer_base_template = host.file(role_dir + '/packer/base-test-images.pkr.hcl')
        assert packer_base_template.exists
        assert packer_base_template.contains('ansible-test-arole-'+str(ccinput["role_name"]))
        assert packer_base_template.contains('  force_delete_snapshot       = true')
        assert packer_base_template.contains('  force_deregister            = true')
        # check packer_vars.hcl
        packer_base_vars = host.file(role_dir + '/packer/base-test-vars.hcl')
        assert packer_base_vars.exists
        assert packer_base_vars.contains('vpc_id    = "'+str(ccinput["vpc_id"])+'"')
        assert packer_base_vars.contains('subnet_id = "'+str(ccinput["subnet_id"])+'"')
        assert packer_base_vars.contains('ami_id    = "'+str(ccinput["ami_id"]))
        # check create_test_vpc.sh
        create_stack_sh = host.file(role_dir + '/scripts/create_test_vpc.sh')
        assert create_stack_sh.exists
        assert create_stack_sh.contains('aws cloudformation create-stack '
                                        '--stack-name "test-arole-'+str(
            ccinput["role_name"])+'"')
        delete_stack_sh = host.file(role_dir + '/scripts/delete_test_vpc.sh')
        assert delete_stack_sh.exists
        assert delete_stack_sh.contains('aws cloudformation delete-stack '
                                        '--stack-name "test-arole-'+str(
            ccinput["role_name"])+'"')
