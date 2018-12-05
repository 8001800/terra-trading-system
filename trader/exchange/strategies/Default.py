# -*- coding: UTF-8 -*-
from exchange.Trading import *


class Default(Trading):

    def next(self, symbol, tick):
        quantity = 1
        sell_price = 0.00006
        self.buy(symbol, quantity, sell_price, self.exchange)


if __name__ == '__main__':
    t = Default()
    t.run()
