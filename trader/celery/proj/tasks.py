from __future__ import absolute_import
import time
from binance.client import Client
from binance.websockets import BinanceSocketManager
from kafka import KafkaProducer
import json
from proj.celery import app
from kafka import TopicPartition
from kafka import KafkaConsumer

def handle_message(msg,producer,symbol):
    print(msg)
    producer.send(symbol, json.dumps(msg))

f = open('config', 'r')
for line in f:
    if line.startswith("binance_key"):
        PUBLIC = line.split("=")[1].replace(" ","").replace("\"","").replace("\n","") 
    if line.startswith("binance_secret"):
        SECRET = line.split("=")[1].replace(" ","").replace("\"","").replace("\n","")   
    if line.startswith("bootstrap_servers"):
        bootstrap_servers = line.split("=")[1].replace(" ","").replace("\"","").replace("\n","")  


#binance_streaming.s('ETHUSDT').apply_async(queue = 'foo1')
@app.task
def binance_streaming(symbol):

    client = Client(api_key=PUBLIC, api_secret=SECRET, requests_params={"timeout": 30})
    bm = BinanceSocketManager(client)
    

    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    #ETHUSDT
    conn_key = bm.start_trade_socket(symbol, callback=lambda msg, producer=producer, symbol: handle_message(msg,producer,symbol))

    
    bm.start()
    #time.sleep(10) # let some data flow..

    #bm.stop_socket(conn_key)

@app.task
def save_to_s3(symbol):
    
    bucketName = "elasticbeanstalk-us-east-1-559984272434"
    Key = "producer.py"
    outPutname = symbol  
    s3 = boto3.client('s3')
    
    consumer = KafkaConsumer(bootstrap_servers='52.23.194.164:9094')
    consumer.subscribe([symbol])
    msg = next(consumer)
    
    s3.upload_file(Key,bucketName,outPutname)
    while msg:
            msg = next(consumer)
            
            s3.upload_file(Key,bucketName,outPutname)
