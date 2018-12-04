# -*- coding: UTF-8 -*-
from app.Trading import *
import math
import talib
import config
from backtrader import Strategy
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
from app.database.MongoDBPipeline import MongoDBPipeline
from app.datafeed.Datafeed import PandasData
import matplotlib

class Default(globals()[config.app_mode]):

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        d=0
    def next(self):
        quantity = 1
        sell_price = 0.00006
        #self.buy(symbol, quantity, sell_price, self.exchange)


def trading():
    t = Default()
    t.run()

def database():
    server = config.server
    port = config.port
    db = config.db
    name = config.name
    passwd = config.passwd
    col = config.col
    conn = MongoDBPipeline(server, port, db, name, passwd, col)
    dd = list(conn.getIds({"symbol": {"$regex": u"smtusdt"}, "period": "1day"}, col))
    data = pd.DataFrame(dd)
    return data

def strategy():
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(Default)

    dataframe = database()

    # Pass it to the backtrader datafeed and add it to the cerebro
    data = PandasData(dataname=dataframe)
    cerebro.adddata(data)

    # Run over everything
    cerebro.run()
    print(1)
    # Plot the result
    cerebro.plot(style='bar')


if __name__ == '__main__':
    globals()[config.app_mode.lower()]()
    #strategy()
