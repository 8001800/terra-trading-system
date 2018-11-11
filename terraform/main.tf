provider "aws" {
  region     = "${var.aws_region}"
  access_key = "${var.aws_access_key}"
  secret_key = "${var.aws_secret_key}"
}

resource "aws_key_pair" "default"{
  key_name = "clusterkp"
  public_key = "${file("${var.public_key_path}")}"
}



resource "aws_instance" "celery" {
  ami             = "${var.aws_ami}"
  instance_type   = "${var.instance_type}"
  key_name        = "${aws_key_pair.default.id}"
  

  security_groups = ["${aws_security_group.ssh.name}", "${aws_security_group.rpc.name}"]
  
  tags {
    Name = "celery"
  }

  connection {
    type        = "ssh"
    user        = "${var.user}"
    private_key = "${file("${var.private_key_path}")}"
  }

   provisioner "remote-exec" {
    inline = [
      "mkdir celery"
    ]
  }

  provisioner "file" {
    source = "../celery/"
    destination = "/home/${var.user}/celery"
  }

  provisioner "remote-exec" {
    script = "${var.bootstrap_path}"
  }

}


resource "aws_instance" "kafka" {
  count           = 1
  ami             = "${var.aws_ami}"
  instance_type   = "${var.instance_type}"
  key_name        = "${aws_key_pair.default.id}"
  
  
  security_groups = ["${aws_security_group.ssh.name}", "${aws_security_group.kafka-node.name}", "${aws_security_group.rpc.name}"]

  tags {
    Name = "kafka-${count.index}"
  }
  connection {
    type         = "ssh"
    
    user         = "${var.user}"
    private_key  = "${file("${var.private_key_path}")}"
    
  }

  provisioner "remote-exec" {
    inline = [
      "mkdir resources",
      "cd  resources",
      "mkdir kafka${count.index}"
    ]
}

  provisioner "file" {
    source = "../resources/kafka${count.index}/"
    destination = "/home/${var.user}/resources/kafka${count.index}/"
  }


  provisioner "remote-exec" {
    script = "${var.bootstrap_path}"
  }
}

