resource "aws_security_group" "ssh" {
  name        = "allow_ssh"
  description = "Allows inbound ssh connections. Also allows all egress connections."

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  
  tags {
    Name = "Web Server SG"
  }
}

resource "aws_security_group" "ssh_private" {
  name        = "allow_ssh_private"
  description = "Allows inbound ssh connections with subnets. Also allows all egress connections."

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  
  tags {
    Name = "Web Server SG"
  }
}

resource "aws_security_group" "https" {
  name        = "allow_https"
  description = "Allows inbount http/s connections"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags {
    Name = "Web Server SG"
}
}

resource "aws_security_group" "kafka-node" {
  name        = "allow_eth-node"
  description = "Allows inbount eth node network connections"

  ingress {
    from_port   = 30303
    to_port     = 30303
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 2181
    to_port     = 2181
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9092
    to_port     = 9092
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 30303
    to_port     = 30303
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  
  tags {
    Name = "Web Server SG"
}
}

resource "aws_security_group" "rpc" {
  name        = "allow_rpc"
  description = "Allows inbount rpc connections"

  ingress {
    from_port   = 8545
    to_port     = 8545
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

 
  tags {
    Name = "Web Server SG"
}
}


