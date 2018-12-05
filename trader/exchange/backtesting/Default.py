# -*- coding: UTF-8 -*-
import config
import backtrader as bt
import pandas as pd
from db import MongoDBPipeline
from exchange.datafeed.Datafeed import PandasData


class Default(bt.Strategy):

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        quantity = 1
        sell_price = 0.00006
        #self.buy(symbol, quantity, sell_price, self.exchange)


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


if __name__ == '__main__':
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

    # Plot the result
    cerebro.plot(style='bar')
