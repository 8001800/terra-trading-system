
class Datafeed:

    @staticmethod
    def tick_feed(symbol, exchange):
        return globals()[exchange].get_ticker(symbol)

    @staticmethod
    def no_feed(symbol, exchange):
        pass