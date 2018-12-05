from __future__ import absolute_import
from binance.client import Client
from binance.websockets import BinanceSocketManager
from kafka import KafkaProducer
import json
from proj.celery import application
from kafka import KafkaConsumer
import boto3
import proj.settings


def handle_message(msg, symb, producer):
    print(msg)
    producer.send(symb, json.dumps(msg))

# binance_streaming.s('ETHUSDT').apply_async(queue = 'foo1')


@application.task
def binance_streaming(symb):
    client = Client(api_key=settings.binance_key, api_secret=settings.binance_secret, requests_params={"timeout": 30})
    bm = BinanceSocketManager(client)
    producer = KafkaProducer(bootstrap_servers=settings.bootstrap_servers,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    # ETHUSDT
    conn_key = bm.start_trade_socket(symb,
                                     callback=lambda msg, symb, producer=producer: handle_message(msg, symb, producer))

    bm.start()
    # time.sleep(10) # let some data flow..

    # bm.stop_socket(conn_key)


@application.task
def save_to_s3(symbol):
    bucketName = "elasticbeanstalk-us-east-1-559984272434"
    Key = "producer.py"
    outPutname = symbol
    s3 = boto3.client('s3')

    consumer = KafkaConsumer(bootstrap_servers='52.23.194.164:9094')
    consumer.subscribe([symbol])
    msg = next(consumer)

    s3.upload_file(Key, bucketName, outPutname)
    while msg:
        msg = next(consumer)

        s3.upload_file(Key, bucketName, outPutname)
