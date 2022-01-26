
import json

from web3 import Web3, HTTPProvider


if __name__ == '__main__':
    w3 =Web3(HTTPProvider(endpoint_uri='HTTP://127.0.0.1:7545'))
    w3.eth.default_account = w3.eth.accounts[0]
    jsonf = open("Greeter.json", 'rb')
    jsobjs = json.load(jsonf)
    #Greeter = w3.eth.contract(abi=jsobjs['abi'], bytecode=jsobjs['bytecode'])
    #Greeter.greeter.functions.greet().call()
    greeter = w3.eth.contract(
        address='0xB5816B1C17ce9386019ac42310dB523749F5f2c3',
        abi=jsobjs['abi']
    )
    #print(greeter.functions.greet().call())
    #print(greeter.functions.greet2(123).call())
    print(greeter.functions.greet3(456).call(sigfn="0xf9220889"))

