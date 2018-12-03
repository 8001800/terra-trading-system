from app.exchanges.TerrachainAPI import *
import json


fo = open("exchanges/abis/Exchange.abi.json", "r")
Exchangeabi=json.load(fo)
fo.close()

fo = open("exchanges/abis/ERC827.abi.json", "r")
ERC827abi=json.load(fo)
fo.close()

CLC_ADDRESS = '0x0000000000000000000000000000000000000000'
rpc_url="https://gaia.terrachain.network"


client = TerrachainAPI(Exchangeabi,ERC827abi,CLC_ADDRESS, rpc_url)

class TerrachainWrapper:

    @staticmethod
    def buy_limit(quantity, buyPrice):
        return client.buy_token(quantity, buyPrice)

    @staticmethod
    def sell_limit(quantity, buyPrice):
        return client.sell_token(quantity, buyPrice)