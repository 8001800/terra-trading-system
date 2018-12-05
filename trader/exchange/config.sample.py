# @yasinkuyu

# Get an Key and Secret 
# https://www.binance.com/restapipub.html

#binance

api_key = ''
api_secret = ''

recv_window = 6000000

#huobi

ACCESS_KEY = ""
SECRET_KEY = ""


#contractland

RPC_URL=""
EXCHANGE_ADDRESS=""
ETH_TOKEN_ADDRESS=""

USER_ADDRESS=""
USER_ADDRESS_PRIVATE_KEY=""
GET_RECEIPT_INTERVAL_IN_MILLISECONDS=3000
GAS_PRICE=1


#exchange database
server = ''
port = 27017
db = ""
name = ''
passwd = ''
col = ''


#parameters
quantity=0                             #Buy/Sell Quantity
amount=0                               #Buy/Sell BTC Amount (Ex: 0.002 BTC)
symbol="ETHUSDT"                       #Market Symbol (Ex: XVGBTC - XVGETH)
profit=1.3                             #Target Profit
stop_loss=0                            #Target Stop-Loss %% (If the price drops by 6%%, sell market_price.)
increasing=0.00000001                  #Buy Price +Increasing (0.00000001)
decreasing=0.00000001                  #Sell Price -Decreasing (0.00000001)

    # Manually defined --orderid try to sell
orderid=0                              #Target Order Id (use balance.py)
wait_time=30                           #Wait Time (seconds)
test_mode=False                        #Test Mode True/False
prints=True                            #Scanning Profit Screen Print True/False
loop=0                                 #Loop (0 unlimited)

    # Working Modes
    #  - profit: Profit Hunter. Find defined profit, buy and sell. (Ex: 1.3% profit)
    #  - range: Between target two price, buy and sell. (Ex: <= 0.00100 buy - >= 0.00150 sell )
mode="profit"                          #Working Mode
buyprice=0                             #Buy Price (Price is greater than equal <=)
sellprice=0                            #Sell Price (Price is less than equal >=)
commision='BNB'                        #Type of commission, TOKEN/BNB (default BNB)
exchange='Terrachain'                  #Select the exchange
datafeed_type='no_feed'                #Type of the datefeed
app_mode="Trading"                     #Trading is the trading mode; Trading is the backtrader mode