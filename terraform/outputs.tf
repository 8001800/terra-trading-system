output "kafka.ip" {
  value = "${join(",",aws_instance.kafka.*.public_ip)}"
}

output "celery.ip" {
  value = "${aws_instance.celery.public_ip}"
}


