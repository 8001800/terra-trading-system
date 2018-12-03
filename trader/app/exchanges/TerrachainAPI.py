from web3 import Web3
import config


class TerrachainAPI:
    
    def __init__(self,Exchangeabi,ERC827abi,trade_token_add, rpc_url):

        self.trade_token_add=trade_token_add
        self.web3Instance = Web3(Web3.HTTPProvider(rpc_url,request_kwargs={'timeout':240}))
        self.erc827 = self.web3Instance.eth.contract(abi=ERC827abi, address=config.ETH_TOKEN_ADDRESS)
        self.exchange = self.web3Instance.eth.contract(abi=Exchangeabi, address=config.EXCHANGE_ADDRESS)


    def buy_token(self,tradeTokenAmount,tradePrice):
        baseTokenAmount = tradeTokenAmount * tradePrice
        nonce = self.web3Instance.eth.getTransactionCount(config.USER_ADDRESS)
        buyData = self.exchange.functions.buy(config.ETH_TOKEN_ADDRESS, self.trade_token_add,  config.USER_ADDRESS, self.web3Instance.toWei(str(tradeTokenAmount),'ether'), self.web3Instance.toWei(str(tradePrice),'ether')).buildTransaction({'gas': 500000, 'gasPrice': self.web3Instance.toWei('1', 'gwei'),'nonce': nonce,})
        txData = self.erc827.functions.approveAndCall(config.EXCHANGE_ADDRESS, self.web3Instance.toWei(baseTokenAmount,'ether'), buyData['data']).buildTransaction({'gas': 500000, 'gasPrice': self.web3Instance.toWei('1', 'gwei'),'nonce': nonce,})
        
        #print(txData)
        
        signed_txn = self.web3Instance.eth.account.signTransaction(txData, private_key=config.USER_ADDRESS_PRIVATE_KEY)
        txhash=self.web3Instance.eth.sendRawTransaction(signed_txn.rawTransaction)   
        return txhash.hex()
      
    def sell_token(self,tradeTokenAmount,tradePrice):
          
        baseTokenAmount = tradeTokenAmount * tradePrice
       
        nonce = self.web3Instance.eth.getTransactionCount(config.USER_ADDRESS)
        
        sellData = self.exchange.functions.sell(config.ETH_TOKEN_ADDRESS, self.trade_token_add,  config.USER_ADDRESS, self.web3Instance.toWei(str(tradeTokenAmount),'ether'), self.web3Instance.toWei(str(tradePrice),'ether')).buildTransaction({'gas': 500000, 'gasPrice': self.web3Instance.toWei('1', 'gwei'),'nonce': nonce,'value': self.web3Instance.toWei(str(tradeTokenAmount),'ether')})
        signed_txn = self.web3Instance.eth.account.signTransaction(sellData, private_key=config.USER_ADDRESS_PRIVATE_KEY)
        txhash=self.web3Instance.eth.sendRawTransaction(signed_txn.rawTransaction)   
        return txhash.hex()

