source "amazon-ebs" "ubuntu" {
  ami_name      = "ansible-test-arole-{{ cookiecutter.role_name }}-{{ "{{" }}timestamp{{ "}}" }}"
  instance_type = "t2.micro"
  region        = "us-east-1"
  vpc_id = "{{ "{{" }}env `VPC_ID`{{ "}}" }}"
  subnet_id = "{{ "{{" }}env `SUBNET_ID`{{ "}}" }}"
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/*ubuntu-focal-20.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"]
  }
  ssh_username = "ubuntu"
  ssh_interface = "public_ip"
  associate_public_ip_address = true
}

build {
  name    = "ansible-test-arole-{{ cookiecutter.role_name }}"

  sources = [
    "source.amazon-ebs.ubuntu"
  ]
  provisioner "shell" {
    script = "install_ubuntu_desktop.sh"
}
}
