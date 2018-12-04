from app.brokers.TerrachainAPI import *
import json


fo = open("../brokers/abis/Exchange.abi.json", "r")
Exchangeabi=json.load(fo)
fo.close()

fo = open("../brokers/abis/ERC827.abi.json", "r")
ERC827abi=json.load(fo)
fo.close()

CLC_ADDRESS = '0x0000000000000000000000000000000000000000'
rpc_url="https://gaia.terrachain.network"


client = TerrachainAPI(Exchangeabi,ERC827abi,CLC_ADDRESS, rpc_url)

class Terrachain:

    @staticmethod
    def buy_limit(symbol,quantity, buyPrice):
        return client.buy_token(quantity, buyPrice)

    @staticmethod
    def sell_limit(symbol,quantity, sellprice):
        return client.sell_token(quantity, sellprice)