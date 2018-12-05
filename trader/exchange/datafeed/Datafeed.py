import backtrader as bt

class Datafeed:

    @staticmethod
    def tick_feed(symbol, exchange):
        return globals()[exchange].get_ticker(symbol)

    @staticmethod
    def no_feed(symbol, exchange):
        pass



class PandasData(bt.feeds.pandafeed.PandasData):
    '''
    The ``dataname`` parameter inherited from ``feed.DataBase`` is the pandas
    DataFrame
    '''

    params = (
        # Possible values for datetime (must always be present)
        #  None : datetime is the "index" in the Pandas Dataframe
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('datetime', "date"),

        # Possible values below:
        #  None : column not present
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', 'close'),
        ('volume', "vol"),
        ('openinterest', None),
    )
