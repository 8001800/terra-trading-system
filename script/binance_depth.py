from binance.websockets import BinanceSocketManager
from binance.depthcache import DepthCacheManager
from binance.client import Client
f = open('config', 'r')
for line in f:
    if line.startswith("binance_key"):
        PUBLIC = line.split("=")[1].replace(" ","").replace("\"","").replace("\n","") 
    if line.startswith("binance_secret"):
        SECRET = line.split("=")[1].replace(" ","").replace("\"","").replace("\n","")   
    if line.startswith("bootstrap_servers"):
        bootstrap_servers = line.split("=")[1].replace(" ","").replace("\"","").replace("\n","")  

def process_depth(depth_cache):
        if depth_cache is not None:
            print("symbol {}".format(depth_cache.symbol))
            print("top 5 bids")
            print(depth_cache.get_bids())
            print("top 5 asks")
            print(depth_cache.get_asks())
        else:
            # depth cache had an error and needs to be restarted
        
        
            depth_cache = dcm.get_depth_cache()
            if depth_cache is not None:
                print("symbol {}".format(depth_cache.symbol))
                print("top 5 bids")
                print(depth_cache.get_bids())
                print("top 5 asks")
                print(depth_cache.get_asks())
            else:
                # depth cache had an error and needs to be restarted
                pass


client = Client(api_key=PUBLIC, api_secret=SECRET)

print(0)
bm = BinanceSocketManager(client)
print(1)

dcm1 = DepthCacheManager(client, 'BNBBTC', callback=process_depth, bm=bm)

print(2)

