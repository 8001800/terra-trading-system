import os
from celery import Celery
import time
from binance.client import Client
from binance.websockets import BinanceSocketManager
from kafka import KafkaProducer
import json

def handle_message(msg,producer):
    print(msg)
    producer.send('topic', json.dumps(msg))

f = open('config', 'r')
for line in f:
    if line.startswith("binance_key"):
        PUBLIC = line.split("=")[1].replace(" ","").replace("\"","").replace("\n","") 
    if line.startswith("binance_secret"):
        SECRET = line.split("=")[1].replace(" ","").replace("\"","").replace("\n","")   
    if line.startswith("bootstrap_servers"):
        bootstrap_servers = line.split("=")[1].replace(" ","").replace("\"","").replace("\n","")  


#producer = KafkaProducer(bootstrap_servers=bootstrap_servers,value_serializer=lambda v: json.dumps(v).encode('utf-8'))


app = Celery('proj',broker="redis://localhost:6379")

app.config_from_object("proj")
#app.conf.result_backend = 'redis://localhost:6379/0'
#app.autodiscover_tasks()
print(bootstrap_servers)

@app.task
def add():

    client = Client(api_key=PUBLIC, api_secret=SECRET, requests_params={"timeout": 30})
    bm = BinanceSocketManager(client)
    

    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    conn_key = bm.start_trade_socket('ETHUSDT', callback=lambda msg, producer=producer: handle_message(msg,producer))

    
    bm.start()
    #time.sleep(10) # let some data flow..

    #bm.stop_socket(conn_key)