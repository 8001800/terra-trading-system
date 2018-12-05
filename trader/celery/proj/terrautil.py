from __future__ import absolute_import
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from db.MongoDBPipeline import MongoDBPipeline
from proj.celery import application
import proj.settings as settings
from web3 import Web3

provider = Web3.HTTPProvider('http://test.terrachain.network')
client = Web3(provider)

host= settings.CELERY_MONGODB_BACKEND_SETTINGS["host"]
port= int(settings.CELERY_MONGODB_BACKEND_SETTINGS["port"])
database= settings.CELERY_MONGODB_BACKEND_SETTINGS["database"]
user= settings.CELERY_MONGODB_BACKEND_SETTINGS["user"]
password= settings.CELERY_MONGODB_BACKEND_SETTINGS["password"]
taskmeta_collection= settings.accounts

conn = MongoDBPipeline(host, port, database, user, password, taskmeta_collection)


@application.task
def create_account():
    acct = client.eth.account.create()
    conn.process_item({"_id":acct.address, "privatekey":acct.privateKey.hex()}, taskmeta_collection)




