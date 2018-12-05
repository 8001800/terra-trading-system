# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import bson
import time


class MongoDBPipeline(object,):
    def __init__(self, server, port, db, name, passwd, col):
        #with key
        self.server = server
        self.port = port
        self.db = db
        self.name = name
        self.passwd =  passwd
        self.col = col
        time.sleep(2)
        self.client = pymongo.MongoClient("mongodb://%s:%s@%s:%s/%s" % (self.name,self.passwd,self.server,self.port,self.db),socketKeepAlive=True)
        self.db_conn = self.client[self.db]
        self.db_conn.authenticate(self.name,self.passwd)

        #self.client = pymongo.MongoClient(self.server, self.port)
        #self.db_conn = self.client[self.db]
        print("connected")

    def process_item(self, item, col):
        #err_msg = ''
        pre_dic = dict(item)
        #col = pre_dic["col"]
        # for field, data in item.items():
        #     if not data:
        #         err_msg += 'Missing %s\n' % (field)
        # if err_msg:
        #     raise DropItem(err_msg)
        try:
            #pre_dic.pop("col")
            self.db_conn[col].insert(pre_dic)
            #log.msg('Item written to MongoDB database %s/%s' % (self.db, col),
            #        level=log.DEBUG, spider=spider)
        except Exception as e:
            #log.msg('Error written to MongoDB database %s/%s' % (self.db, col),
            #        level=log.DEBUG, spider=spider)
            pass
        #return item
    #without key
    def open_connection(self, mongo_db):
        self.client = pymongo.MongoClient(self.host, self.port)
        self.db = self.client[mongo_db]
        print("connected")

    def close_connection(self):
        self.client.close()

#     def process_item(self, item, collection_name):
#         self.db_conn[collection_name].insert(item)
#         return item
    def updateItems(self,collection_name,_id,field_name,data):
        collection = self.db_conn[collection_name]

        collection.update({"_id":_id},{"$set":{field_name:data}})

    def updateItems_all(self,collection_name,_id,data):
        collection = self.db_conn[collection_name]

        collection.update({"_id":_id},data)    
    
    def pageget(self, start, limit, collection_name):
        collection = self.db_conn[collection_name]
        return collection.find().limit(limit).skip(start)

    def getIds(self, dict,collection_name,filt=None):
        collection = self.db_conn[collection_name]
        return collection.find(dict,filt,no_cursor_timeout=True)

    def getStocks(self, collection_name):
        collection = self.db_conn[collection_name]
        return collection.find({},{'_id':1,"name":1}).batch_size(1000)
    
    def GetNation(self, collection_name, key, value):
        return self.db_conn[collection_name].find_one({key: value})

    def existsornot(self, collection_name, id):
        ting = self.db_conn[collection_name].find_one({'_id': id})
        if ting == None:
            return 0
        else:
            return 1

    def existsornot2(self, collection_name, id):
        ting = self.db_conn[collection_name].find_one({'_id': id})
        if ting == None:
            return False
        else:
            return ting

    def findDistinct(self,key,collection_name):
        collection = self.db_conn[collection_name]
        return collection.distinct(key)