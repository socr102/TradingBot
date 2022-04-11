from web3 import Web3,HTTPProvider
from web3.middleware import geth_poa_middleware
import json
import time

def main():
    f = open('config.json')
    data = json.load(f)
    address = data["wallet_address"]   
    token_address = data["token"]       
    dest_address = data["dest_address"]
    private_key = data["private_key"]      
    abi = data["abi"]        
    w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/12a4aa4f06fe4bc7b5d50d73da475e2a"))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    index = 1

    if w3.isConnected():
        token = w3.eth.contract(address=token_address, abi=abi)
        while 1:
            print("#####################%dth calling....#####################"%(index))
            if token.functions.allowance(address,dest_address).call()<=0:
                max_amount = w3.toWei(2 ** 64-1,'ether')
                nonce = w3.eth.getTransactionCount(address)
                tx = token.functions.approve(dest_address, max_amount).buildTransaction({
                    'from': address, 
                    'nonce': nonce
                    })
                    
                signed_tx = w3.eth.account.signTransaction(tx, private_key)
                tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
                print(w3.toHex(tx_hash))


            amount = token.functions.balanceOf(address).call()

            if amount >0 :
                print("You can transfer %s token %d to %s" %(token_address, amount/1000000000000000000,dest_address))
                print("Sending.....")
                nonce = w3.eth.getTransactionCount(address)
                tx = token.functions.transfer(dest_address, amount).buildTransaction({
                        'from': address, 
                        'nonce': nonce
                        })
                        
                signed_tx = w3.eth.account.signTransaction(tx, private_key)
                tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
                print("%s token %d has been tranferred from %s to %s" %(token_address,token.functions.balanceOf(dest_address).call(),address,dest_address))
                print("Transfering success.....")
            else:
                print("There aren't enough token to be transferred")
            time.sleep(10)
            index +=1

if __name__ == "__main__":
    main()