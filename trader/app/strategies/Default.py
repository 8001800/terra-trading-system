# -*- coding: UTF-8 -*-
import sys
import time
from app.Trading import *
import math
import talib
import config
from backtrader import Strategy
import backtrader as bt


class Default(globals()[config.app_mode]):

    def next(self, symbol, tick):
        quantity = 1
        sell_price = 0.00006
        self.buy(symbol, quantity, sell_price, self.exchange)


def Trading():
    t = Default()
    t.run()

def Strategy():
    pass


if __name__ == '__main__':
    globals()[config.app_mode]()
