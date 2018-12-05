import json
from brokers.TerrachainAPI import TerrachainAPI

import os
script_dir = os.path.dirname(os.path.dirname(__file__)) #<-- absolute dir the script is in

rel_path_exchange = "brokers/abis/Exchange.abi.json"
abs_file_path_exchange = os.path.join(script_dir, rel_path_exchange)
print(abs_file_path_exchange)
fo = open(abs_file_path_exchange, "r")
Exchangeabi=json.load(fo)
fo.close()


rel_path_827 = "brokers/abis/ERC827.abi.json"
abs_file_path_827 = os.path.join(script_dir, rel_path_exchange)
fo = open(abs_file_path_827, "r")
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