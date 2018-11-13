# Terra Trading System

## Notes

1. Start Kafka nodes: go to resources/kafka*/docker-compose.yml replace KAFKA_ADVERTISED_HOST_NAME with your Kafka host IP
2. Connect Celery and Kafka: go to  celery/config replace bootstrap_servers with your Kafka host IP
3. Kafka image: https://github.com/wurstmeister/kafka-docker
4. Kafka Spark-streaming Cassandra image: https://github.com/Yannael/kafka-sparkstreaming-cassandra
5. Celery image: https://github.com/williln/celery-docker-example

