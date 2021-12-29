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
            extra_context={
                "role_name": ccinput["role_name"],
                "vpc_id": ccinput["vpc_id"],
                "subnet_id": ccinput["subnet_id"],
                "ami_id": ccinput["ami_id"],
                },
        )
        #  .env file exists
        env_file = host.file(role_dir + '/.env')
        assert env_file.exists
        assert env_file.contains('^export VPC_ID='+str(ccinput["vpc_id"]))
        assert env_file.contains('^export SUBNET_ID='+str(ccinput["subnet_id"]))
        assert env_file.contains('^export AMI_ID='+str(ccinput["ami_id"]))
