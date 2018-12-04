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
LOGGER_FILE = "binance-trader.log"
FORMAT = '%(asctime)-15s - %(levelname)s:  %(message)s'

logger = logging.basicConfig(filename=LOGGER_FILE, filemode='a',
                             format=formater_str, datefmt=datefmt,
                             level=logging.INFO)

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

        # setup Logger
        self.logger =  self.setup_logger(config.symbol, debug=config.debug)

    def setup_logger(self, symbol, debug=True):
        """Function setup as many loggers as you want"""
        #handler = logging.FileHandler(log_file)
        #handler.setFormatter(formatter)
        #logger.addHandler(handler)
        logger = logging.getLogger(symbol)

        stout_handler = logging.StreamHandler(sys.stdout)
        if debug:
            logger.setLevel(logging.DEBUG)
            stout_handler.setLevel(logging.DEBUG)

        #handler = logging.handlers.SysLogHandler(address='/dev/log')
        #logger.addHandler(handler)
        stout_handler.setFormatter(formatter)
        logger.addHandler(stout_handler)
        return logger

    def buy(self, symbol, quantity, buyPrice, exchange):
        try:
            # Create order
            orderId = globals()[exchange].buy_limit(symbol, quantity, buyPrice)

            #print('Buy order created id:%d, q:%.8f, p:%.8f' % (orderId, quantity, float(buyPrice)))
            self.logger.info('%s : Buy order created , q:%.8f, p:%.8f' % (symbol, quantity, float(buyPrice)))
            #self.order_id = orderId
            #return orderId

        except Exception as e:
            self.logger.debug('Buy error: %s' % (e))
            time.sleep(self.WAIT_TIME_BUY_SELL)
            return None

    def sell(self, symbol, quantity, sell_price, exchange):
        try:
            # Create order
            orderId = globals()[exchange].sell_limit(symbol, quantity, sell_price)

            # print('Buy order created id:%d, q:%.8f, p:%.8f' % (orderId, quantity, float(buyPrice)))
            self.logger.info(
                '%s : Buy order created , q:%.8f, p:%.8f' % (symbol, quantity, float(sell_price)))
            #self.order_id = orderId
            #return orderId

        except Exception as e:
            self.logger.debug('Buy error: %s' % (e))
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
            locals()[exchange].cancel_order(symbol, orderId)
            self.order_id = 0
            self.order_data = None
            return True

    def check_order(self):
        # If there is an open order, exit.
        if self.order_id > 0:
            exit(1)

    def logic(self):
        return 0

    def filters(self):

        symbol = config.symbol

        # Get symbol exchange info
        symbol_info = Binance.get_info(symbol)

        if not symbol_info:
            #print('Invalid symbol, please try again...')
            self.logger.error('Invalid symbol, please try again...')
            exit(1)

        symbol_info['filters'] = {item['filterType']: item for item in symbol_info['filters']}

        return symbol_info

    def format_step(self, quantity, stepSize):
        return float(stepSize * math.floor(float(quantity)/stepSize))

    def validate(self):

        valid = True
        symbol = config.symbol
        filters = self.filters()['filters']

        # Order book prices
        lastBid, lastAsk = Binance.get_order_book(symbol)

        lastPrice = Binance.get_ticker(symbol)

        minQty = float(filters['LOT_SIZE']['minQty'])
        minPrice = float(filters['PRICE_FILTER']['minPrice'])
        minNotional = float(filters['MIN_NOTIONAL']['minNotional'])
        quantity = float(config.quantity)

        # stepSize defines the intervals that a quantity/icebergQty can be increased/decreased by.
        stepSize = float(filters['LOT_SIZE']['stepSize'])

        # tickSize defines the intervals that a price/stopPrice can be increased/decreased by
        tickSize = float(filters['PRICE_FILTER']['tickSize'])

        # If option increasing default tickSize greater than
        if (float(config.increasing) < tickSize):
            self.increasing = tickSize

        # If option decreasing default tickSize greater than
        if (float(config.decreasing) < tickSize):
            self.decreasing = tickSize

        # Just for validation
        lastBid = lastBid + self.increasing

        # Set static
        # If quantity or amount is zero, minNotional increase 10%
        quantity = (minNotional / lastBid)
        quantity = quantity + (quantity * 10 / 100)
        notional = minNotional

        if self.amount > 0:
            # Calculate amount to quantity
            quantity = (self.amount / lastBid)

        if self.quantity > 0:
            # Format quantity step
            quantity = self.quantity

        quantity = self.format_step(quantity, stepSize)
        notional = lastBid * float(quantity)

        # Set Globals
        self.quantity = quantity
        self.step_size = stepSize

        # minQty = minimum order quantity
        if quantity < minQty:
            #print('Invalid quantity, minQty: %.8f (u: %.8f)' % (minQty, quantity))
            self.logger.error('Invalid quantity, minQty: %.8f (u: %.8f)' % (minQty, quantity))
            valid = False

        if lastPrice < minPrice:
            #print('Invalid price, minPrice: %.8f (u: %.8f)' % (minPrice, lastPrice))
            self.logger.error('Invalid price, minPrice: %.8f (u: %.8f)' % (minPrice, lastPrice))
            valid = False

        # minNotional = minimum order value (price * quantity)
        if notional < minNotional:
            #print('Invalid notional, minNotional: %.8f (u: %.8f)' % (minNotional, notional))
            self.logger.error('Invalid notional, minNotional: %.8f (u: %.8f)' % (minNotional, notional))
            valid = False

        if not valid:
            exit(1)

    def action(self):
        pass

    def run(self):

        cycle = 0
        actions = []

        symbol = config.symbol


        print('\n')

        # Validate symbol
        self.validate()

        print('Started...')
        print('Trading Symbol: %s' % symbol)
        print('Buy Quantity: %.8f' % self.quantity)
        print('Stop-Loss Amount: %s' % self.stop_loss)
        #print('Estimated profit: %.8f' % (self.quantity*config.profit))

        if config.mode == 'range':

           if config.buyprice == 0 or config.sellprice == 0:
               print('Please enter --buyprice / --sellprice\n')
               exit(1)

           print('Range Mode Options:')
           print('\tBuy Price: %.8f', config.buyprice)
           print('\tSell Price: %.8f', config.sellprice)

        else:
            print('Profit Mode Options:')
            print('\tPreferred Profit: %0.2f%%' % config.profit)
            print('\tBuy Price : (Bid+ --increasing %.8f)' % self.increasing)
            print('\tSell Price: (Ask- --decreasing %.8f)' % self.decreasing)

        print('\n')

        startTime = time.time()

        """
        # DEBUG LINES
        actionTrader = threading.Thread(target=self.action, args=(symbol,))
        actions.append(actionTrader)
        actionTrader.start()

        endTime = time.time()

        if endTime - startTime < self.wait_time:

            time.sleep(self.wait_time - (endTime - startTime))

            # 0 = Unlimited loop
            if config.loop > 0:
                cycle = cycle + 1

        """

        while (cycle <= config.loop):

            startTime = time.time()
            tick=getattr(Datafeed, config.datafeed_type)(symbol, self.exchange)
            actionTrader = threading.Thread(target=self.action, args=(symbol,tick))
            actions.append(actionTrader)
            actionTrader.start()

            endTime = time.time()

            if endTime - startTime < self.wait_time:

                time.sleep(self.wait_time - (endTime - startTime))

                # 0 = Unlimited loop
                if config.loop > 0:
                    cycle = cycle + 1
