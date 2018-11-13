# Terra Trading System

## Notes

1. Start Kafka nodes: go to resources/kafka*/docker-compose.yml replace KAFKA_ADVERTISED_HOST_NAME with your Kafka host IP
2. Connect Celery and Kafka: go to  celery/config replace bootstrap_servers with your Kafka host IP
3. Kafka image: https://github.com/wurstmeister/kafka-docker
4. Kafka Spark-streaming Cassandra image: https://github.com/Yannael/kafka-sparkstreaming-cassandra
5. Celery image: https://github.com/williln/celery-docker-example

## Reference
1. Celery multi workers example: http://zerosre.com/2017/06/05/celery%E5%A4%9A%E4%B8%AAworker/
2. kafka：https://segmentfault.com/a/1190000015627478
http://www.ligen.pro/2018/01/02/Docker%20Compose%E6%90%AD%E5%BB%BA%E7%AE%80%E5%8D%95Kafka%E9%9B%86%E7%BE%A4/
http://www.uml.org.cn/bigdata/201801112.asp
3. celery config file: https://stackoverflow.com/questions/4763072/why-cant-it-find-my-celery-config-file

