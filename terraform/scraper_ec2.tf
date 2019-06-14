provider "aws" {
  region     = "us-east-1"
}

resource "aws_instance" "scraper_server" {
  ami           = "ami-2757f631"
  instance_type = "t2.micro"
  key_name      = "deployer-key"

  vpc_security_group_ids = [
    "${aws_security_group.allow_inbound_ssh.id}",
    "${aws_security_group.allow_outbound_http.id}"
  ]

  connection {
    type = "ssh"
    user = "ubuntu"
    private_key = "${file("~/.ssh/id_rsa")}"
  }

  provisioner "remote-exec" {
    script      = "../install.sh"
  }
}

resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = "${file("~/.ssh/id_rsa.pub")}"
}

resource "aws_security_group" "allow_inbound_ssh" {
  name        = "allow_inbound_ssh"
  description = "Allow ssh inbound traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
    description = "Allow ssh"
  }
}

resource "aws_security_group" "allow_outbound_http" {
  name        = "allow_outbound_http"
  description = "Allow outbound http and https traffic"

  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
    description = "Allow http"
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
    description = "Allow https"
  }
}

output "public_dns" {
  value = "${aws_instance.scraper_server.public_dns}"
}
