# call smart contract method without abi file

## Origin
A few days ago, I answered a question, and I felt it was okay, so I wrote an article to record it.
The problem is:

[如何用web3py调用闭源合约 | 登链社区 | 技术问答 (learnblockchain.cn)](https://learnblockchain.cn/question/3036)


The transaction mentioned in the question is recorded in 
[Binance Transaction Hash (Txhash) Details | BscScan](https://bscscan.com/tx/0xa3c53ab27fda6f341f2caefeb356051e1de56e27549a586c79fbc67209a9c53d)

First check the transaction record, bscscan cannot parse out the function name, that is, abi is not public. 

## Determine the function call signature 

![16435424371.png](https://img.learnblockchain.cn/attachments/2022/01/qIG80oeX61f677b18a899.png)
That is 0xb45112b2 

1. Search the signature database on the Internet: 

https://www.4byte.directory/signatures/

The search results are as follows: 
![16435427511.png](https://img.learnblockchain.cn/attachments/2022/01/tR0okdU661f678e940259.png)
Indicates that there is no abi definition for the upload function 
2. Without the abi information of the function, is there no way to call it?
of course not!
Just finding the definition of the function is equivalent to defining a function pointer, the signature is just the function pointer, the parameters of the function ensure that the call stack does not go wrong, and we have the function signature. 
3. Find the function prototype, find the contract
Click on the contract address 0x217 this 
![16435431711.png](https://img.learnblockchain.cn/attachments/2022/01/2kqdbfCa61f67a8f55e27.png)
The contract code is not public 
![16435432541.png](https://img.learnblockchain.cn/attachments/2022/01/M244o5Fc61f67ae1d3bcf.png)
click bytecode-decompiler, get code like this:
![16435433551.png](https://img.learnblockchain.cn/attachments/2022/01/eA0LgbWg61f67b42895a4.png)
Search function signature, get function prototype 
```
def unknownb45112b2(uint256 _param1): # not payable
	require calldata.size - 4 >=′ 32
	require _param1 == _param1
	require ext_code.size(heroContractAddress)
```
4. Build functions with different function names and the same function parameters
This function has a return value, just to facilitate the demonstration effect 

```
function greet3(uint256 num) public view returns (string memory) {
        return "greet3";
    }
```
Generate the calling interface with your contract
When used, address is the contract address 

```
greeter = w3.eth.contract(
    address='0xB5816B1C17ce9386019ac42310dB523749F5f2c3',
    abi=jsobjs['abi']
)
```
Then call the method 

## fix the problem

1. Looking at the code of webpy, it is obvious that such a call is not supported.
2. Modify the code of webpy yourself to support signature replacement
My open source code provides, modified, [contract.py](https://github.com/daodao2007/e001/blob/master/contract.py "contract.py")

Replace it and use it. 
There are modification instructions on github.
There is an example in the code, a contract provides two functions, the function signature

```
function greet2(uint256 num) public view returns (string memory) {
        return "greet2";
    }

    function greet3(uint256 num) public view returns (string memory) {
        return "greet3";
    }
```

```
* greet2 function signature '0xf9220889'
* greet3  function signature '0x02d355dc'
```

Print 
```
greet2
```

The open source code is at:

[daodao2007/e001: call smart contract method without abi file (github.com)](https://github.com/daodao2007/e001)

If you need other languages and frameworks, please contact me. 