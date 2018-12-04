#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @yasinkuyu

import sys
sys.path.insert(0, './app')
from app.brokers.BinanceAPI import BinanceAPI
import config

class Binance:

    def __init__(self):
        self.client = BinanceAPI(config.api_key, config.api_secret)



try:

    m = Binance()

    print('1 -) Print orders')
    print('2 -) Scan profits')
    print('3 -) List balances')
    print('4 -) Check balance')
    print('Enter option number: Ex: 2')

    option = input()

    if option is '1':

        print('Enter symbol: Ex: XVGBTC')

        symbol = input()

        # Orders
        print('%s Orders' % (symbol))
        m.orders(symbol, 10)

    elif option is '3':
        m.balances()
    elif option is '4':

        print('Enter asset: Ex: BTC')

        symbol = input()

        print('%s balance' % (symbol))

        m.balance(symbol)
    else:

        print('Enter Asset (Ex: BTC, ETC, BNB, USDT)')

        asset = input()

        print('Profits scanning...')
        m.profits(asset)

except Exception as e:
    print('Exception: %s' % e)
