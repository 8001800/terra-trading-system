# -*- coding: UTF-8 -*-
import sys
import time
from app.Trading import *
import math


class Default(Trading):

    def action(self, symbol, tick):
        quantity = 1
        sell_price = 0.00006
        self.buy(symbol, quantity, sell_price, self.exchange)
