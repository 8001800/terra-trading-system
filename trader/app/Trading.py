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
from wrapper.BinanceWrapper import BinanceWrapper
from wrapper.HuobiWrapper import HuobiWrapper


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

    def __init__(self, option):
        print("options: {0}".format(option))

        # Get argument parse options
        self.option = option

        # Define parser vars
        self.order_id = self.option.orderid
        self.quantity = self.option.quantity
        self.wait_time = self.option.wait_time
        self.stop_loss = self.option.stop_loss

        self.increasing = self.option.increasing
        self.decreasing = self.option.decreasing

        # BTC amount
        self.amount = self.option.amount

        # Type of commision
        if self.option.commision == 'TOKEN':
            self.commision = TOKEN_COMMISION

        # setup Logger
        self.logger =  self.setup_logger(self.option.symbol, debug=self.option.debug)

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


    def buy(self,symbol,quantity,buyPrice,exchange):

        try:
            # Create order
            orderId = locals()[exchange].buy_limit(symbol, quantity, buyPrice)

            #print('Buy order created id:%d, q:%.8f, p:%.8f' % (orderId, quantity, float(buyPrice)))
            self.logger.info('%s : Buy order created id:%d, q:%.8f, p:%.8f' % (symbol, orderId, quantity, float(buyPrice)))
            self.order_id = orderId
            return orderId

        except Exception as e:
            self.logger.debug('Buy error: %s' % (e))
            time.sleep(self.WAIT_TIME_BUY_SELL)
            return None

    def sell(self, symbol, quantity, orderId, sell_price, last_price, exchange):
        try:
            # Create order
            orderId = locals()[exchange].sell_limit(symbol, quantity, sell_price)

            # print('Buy order created id:%d, q:%.8f, p:%.8f' % (orderId, quantity, float(buyPrice)))
            self.logger.info(
                '%s : Buy order created id:%d, q:%.8f, p:%.8f' % (symbol, orderId, quantity, float(sell_price)))
            self.order_id = orderId
            return orderId

        except Exception as e:
            self.logger.debug('Buy error: %s' % (e))
            time.sleep(self.WAIT_TIME_BUY_SELL)
            return None

    def stop(self, symbol, quantity, orderId, last_price,exchange):
        # If the target is not reached, stop-loss.
        stop_order = locals()[exchange].get_order(symbol, orderId)

        stopprice =  self.calc(float(stop_order['price']))

        lossprice = stopprice - (stopprice * self.stop_loss / 100)

        status = stop_order['status']

        # Order status
        if status == 'NEW' or status == 'PARTIALLY_FILLED':

            if self.cancel(symbol, orderId):

                # Stop loss
                if last_price >= lossprice:

                    sello = locals()[exchange].sell_market(symbol, quantity)

                    #print('Stop-loss, sell market, %s' % (last_price))
                    self.logger.info('Stop-loss, sell market, %s' % (last_price))

                    sell_id = sello['orderId']

                    if sello == True:
                        return True
                    else:
                        # Wait a while after the sale to the loss.
                        time.sleep(self.WAIT_TIME_STOP_LOSS)
                        statusloss = sello['status']
                        if statusloss != 'NEW':
                            print('Stop-loss, sold')
                            self.logger.info('Stop-loss, sold')
                            return True
                        else:
                            self.cancel(symbol, sell_id)
                            return False
                else:
                    sello = locals()[exchange].sell_limit(symbol, quantity, lossprice)
                    sell_id = sello['orderId']
                    print('Stop-loss, sell limit, %s' % (lossprice))
                    time.sleep(self.WAIT_TIME_STOP_LOSS)
                    statusloss = sello['status']
                    if statusloss != 'NEW':
                        print('Stop-loss, sold')
                        return True
                    else:
                        self.cancel(symbol, sell_id)
                        return False
            else:
                print('Cancel did not work... Might have been sold before stop loss...')
                return True

        elif status == 'FILLED':
            self.order_id = 0
            self.order_data = None
            print('Order filled')
            return True
        else:
            return False

    def check(self, symbol, orderId, quantity, exchange):
        # If profit is available and there is no purchase from the specified price, take it with the market.

        # Do you have an open order?
        self.check_order()

        trading_size = 0
        time.sleep(self.WAIT_TIME_BUY_SELL)

        while trading_size < self.MAX_TRADE_SIZE:

            # Order info
            order = locals()[exchange].get_order(symbol, orderId)

            side  = order['side']
            price = float(order['price'])

            # TODO: Sell partial qty
            orig_qty = float(order['origQty'])
            self.buy_filled_qty = float(order['executedQty'])

            status = order['status']

            #print('Wait buy order: %s id:%d, price: %.8f, orig_qty: %.8f' % (symbol, order['orderId'], price, orig_qty))
            self.logger.info('Wait buy order: %s id:%d, price: %.8f, orig_qty: %.8f' % (symbol, order['orderId'], price, orig_qty))

            if status == 'NEW':

                if self.cancel(symbol, orderId):

                    buyo = locals()[exchange].buy_market(symbol, quantity)

                    #print('Buy market order')
                    self.logger.info('Buy market order')

                    self.order_id = buyo['orderId']
                    self.order_data = buyo

                    if buyo == True:
                        break
                    else:
                        trading_size += 1
                        continue
                else:
                    break

            elif status == 'FILLED':
                self.order_id = order['orderId']
                self.order_data = order
                #print('Filled')
                self.logger.info('Filled')
                break
            elif status == 'PARTIALLY_FILLED':
                #print('Partial filled')
                self.logger.info('Partial filled')
                break
            else:
                trading_size += 1
                continue

    def cancel(self, symbol, orderId, exchange):
        # If order is not filled, cancel it.
        check_order = locals()[exchange].get_order(symbol, orderId)

        if not check_order:
            self.order_id = 0
            self.order_data = None
            return True

        if check_order['status'] == 'NEW' or check_order['status'] != 'CANCELLED':
            locals()[exchange].cancel_order(symbol, orderId)
            self.order_id = 0
            self.order_data = None
            return True

    def calc(self, lastBid):
        try:

            #Estimated sell price considering commision
            return lastBid + (lastBid * self.option.profit / 100) + (lastBid *self.commision)
            #return lastBid + (lastBid * self.option.profit / 100)

        except Exception as e:
            print('Calc Error: %s' % (e))
            return

    def check_order(self):
        # If there is an open order, exit.
        if self.order_id > 0:
            exit(1)

    def action(self, symbol):
        pass

    def logic(self):
        return 0

    def filters(self):

        symbol = self.option.symbol

        # Get symbol exchange info
        symbol_info = BinanceWrapper.get_info(symbol)

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
        symbol = self.option.symbol
        filters = self.filters()['filters']

        # Order book prices
        lastBid, lastAsk = BinanceWrapper.get_order_book(symbol)

        lastPrice = BinanceWrapper.get_ticker(symbol)

        minQty = float(filters['LOT_SIZE']['minQty'])
        minPrice = float(filters['PRICE_FILTER']['minPrice'])
        minNotional = float(filters['MIN_NOTIONAL']['minNotional'])
        quantity = float(self.option.quantity)

        # stepSize defines the intervals that a quantity/icebergQty can be increased/decreased by.
        stepSize = float(filters['LOT_SIZE']['stepSize'])

        # tickSize defines the intervals that a price/stopPrice can be increased/decreased by
        tickSize = float(filters['PRICE_FILTER']['tickSize'])

        # If option increasing default tickSize greater than
        if (float(self.option.increasing) < tickSize):
            self.increasing = tickSize

        # If option decreasing default tickSize greater than
        if (float(self.option.decreasing) < tickSize):
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

    def run(self):

        cycle = 0
        actions = []

        symbol = self.option.symbol


        print('\n')

        # Validate symbol
        self.validate()

        print('Started...')
        print('Trading Symbol: %s' % symbol)
        print('Buy Quantity: %.8f' % self.quantity)
        print('Stop-Loss Amount: %s' % self.stop_loss)
        #print('Estimated profit: %.8f' % (self.quantity*self.option.profit))

        if self.option.mode == 'range':

           if self.option.buyprice == 0 or self.option.sellprice == 0:
               print('Please enter --buyprice / --sellprice\n')
               exit(1)

           print('Range Mode Options:')
           print('\tBuy Price: %.8f', self.option.buyprice)
           print('\tSell Price: %.8f', self.option.sellprice)

        else:
            print('Profit Mode Options:')
            print('\tPreferred Profit: %0.2f%%' % self.option.profit)
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
            if self.option.loop > 0:
                cycle = cycle + 1

        """

        while (cycle <= self.option.loop):

           startTime = time.time()

           actionTrader = threading.Thread(target=self.action, args=(symbol,))
           actions.append(actionTrader)
           actionTrader.start()

           endTime = time.time()

           if endTime - startTime < self.wait_time:

               time.sleep(self.wait_time - (endTime - startTime))

               # 0 = Unlimited loop
               if self.option.loop > 0:
                   cycle = cycle + 1
