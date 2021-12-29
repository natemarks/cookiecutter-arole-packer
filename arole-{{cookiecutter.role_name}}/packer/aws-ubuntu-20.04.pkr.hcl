variable "vpc_id" {
  type    = string
}

variable "subnet_id" {
  type    = string
}

variable "ami_id" {
  type    = string
  default = "default"
}

source "amazon-ebs" "ubuntu" {
  ami_name      = "ansible-test-arole-{{ cookiecutter.role_name }}-{{ "{{" }}timestamp{{ "}}" }}"
  instance_type = "t2.micro"
  region        = "us-east-1"
  vpc_id = "${var.vpc_id}"
  subnet_id = "${var.subnet_id}"
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
