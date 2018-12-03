from app.exchanges.BinanceAPI import *
import config

client = BinanceAPI(config.api_key, config.api_secret)

class BinanceWrapper(BinanceAPI):

    @staticmethod
    def get_kline(market, limit=50):
        return client.get_history(market, limit=50)

