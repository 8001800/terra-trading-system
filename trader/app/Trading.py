# -*- coding: UTF-8 -*-
# @yasinkuyu

# Define Python imports
import sys
import time
import threading
import math
import logging
import logging.handlers


# Define Custom imports
from Database import Database
from wrapper.Binance import Binance
from wrapper.Huobi import Huobi
from wrapper.Terrachain import Terrachain
from app.datafeed.Datafeed import Datafeed
import config


formater_str = '%(asctime)s,%(msecs)d %(levelname)s %(name)s: %(message)s'
formatter = logging.Formatter(formater_str)
datefmt="%Y-%b-%d %H:%M:%S"

LOGGER_ENUM = {'debug':'debug.log', 'trading':'trades.log','errors':'general.log'}
#LOGGER_FILE = LOGGER_ENUM['pre']

FORMAT = '%(asctime)-15s - %(levelname)s:  %(message)s'



# Aproximated value to get back the commision for sell and buy
TOKEN_COMMISION = 0.001
BNB_COMMISION   = 0.0005
#((eth*0.05)/100)


class Trading:
    # Define trade vars  
    order_id = 0
    order_data = None

    buy_filled = True
    sell_filled = True

    buy_filled_qty = 0
    sell_filled_qty = 0

    # percent (When you drop 10%, sell panic.)
    stop_loss = 0

    # Buy/Sell qty
    quantity = 0

    # BTC amount
    amount = 0

    # float(step_size * math.floor(float(free)/step_size))
    step_size = 0

    # Define static vars
    WAIT_TIME_BUY_SELL = 1 # seconds
    WAIT_TIME_CHECK_BUY_SELL = 0.2 # seconds
    WAIT_TIME_CHECK_SELL = 5 # seconds
    WAIT_TIME_STOP_LOSS = 20 # seconds

    MAX_TRADE_SIZE = 7 # int

    # Type of commision, Default BNB_COMMISION
    commision = BNB_COMMISION

    def __init__(self):

        # Define parser vars
        self.order_id = config.orderid
        self.quantity = config.quantity
        self.wait_time = config.wait_time
        self.stop_loss = config.stop_loss
        self.exchange = config.exchange
        self.increasing = config.increasing
        self.decreasing = config.decreasing

        # BTC amount
        self.amount = config.amount

        # Type of commision
        if config.commision == 'TOKEN':
            self.commision = TOKEN_COMMISION

    def buy(self, symbol, quantity, buyPrice, exchange):
        try:
            # Create order
            orderId = globals()[exchange].buy_limit(symbol, quantity, buyPrice)
            #self.order_id = orderId
            #return orderId

        except Exception as e:
            time.sleep(self.WAIT_TIME_BUY_SELL)
            return None

    def sell(self, symbol, quantity, sell_price, exchange):
        try:
            # Create order
            orderId = globals()[exchange].sell_limit(symbol, quantity, sell_price)
            #self.order_id = orderId
            #return orderId

        except Exception as e:
            time.sleep(self.WAIT_TIME_BUY_SELL)
            return None

    def check(self, symbol, orderId, quantity, exchange):
        pass

    def cancel(self, symbol, orderId, exchange):
        # If order is not filled, cancel it.
        check_order = globals()[exchange].get_order(symbol, orderId)

        if not check_order:
            self.order_id = 0
            self.order_data = None
            return True

        if check_order['status'] == 'NEW' or check_order['status'] != 'CANCELLED':
            globals()[exchange].cancel_order(symbol, orderId)
            self.order_id = 0
            self.order_data = None
            return True

    def check_order(self):
        # If there is an open order, exit.
        if self.order_id > 0:
            exit(1)

    def logic(self):
        return 0

    def next(self):
        pass

    def run(self):

        cycle = 0
        actions = []

        symbol = config.symbol

        print('\n')
        print('Started...')
        print('Trading Symbol: %s' % symbol)
        print('Stop-Loss Amount: %s' % self.stop_loss)

        while (cycle <= config.loop):
            startTime = time.time()
            tick=getattr(Datafeed, config.datafeed_type)(symbol, self.exchange)
            actionTrader = threading.Thread(target=self.next, args=(symbol, tick))
            actions.append(actionTrader)
            actionTrader.start()

            endTime = time.time()

            if endTime - startTime < self.wait_time:

                time.sleep(self.wait_time - (endTime - startTime))

                # 0 = Unlimited loop
                if config.loop > 0:
                    cycle = cycle + 1
