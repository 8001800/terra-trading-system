output "kafka.ip" {
  value = "${join(",",aws_instance.kafka.*.public_ip)}"
}

output "spark.ip" {
  value = "${aws_instance.spark.public_ip}"
}


