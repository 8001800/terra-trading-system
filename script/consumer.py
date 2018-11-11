from kafka import TopicPartition
from kafka import KafkaConsumer
consumer = KafkaConsumer(bootstrap_servers='52.91.72.219:9092')
consumer.subscribe(['topic'])
for message in consumer:
            print (message)