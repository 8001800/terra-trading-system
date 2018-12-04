from app.exchanges.HuobiServices import *


class Huobi:

    def __init__(self):
        pass

    @staticmethod
    def get_history(symbol, period, size=150):
        return get_kline(symbol, period, size=150)

    @staticmethod
    def get_depth(symbol, type):
        return get_depth(symbol, type)

