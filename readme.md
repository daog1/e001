# 在没有abi文件的情况下调用智能合约方法
call smart contract method without abi file 

python实现

仓库包含，用到的智能合约，和修改好的,web3py contract.py文件

我的例子里面，
* greet2 函数签名 '0xf9220889'
* greet3  函数签名 '0x02d355dc' 
* 例子是用greet2的函数签名调用的 greet3的函数，用本地的测试链测试成功。

## 参考文档
* [documentation](https://web3py.readthedocs.io/en/latest/)
* [交易记录](https://bscscan.com/tx/0xa3c53ab27fda6f341f2caefeb356051e1de56e27549a586c79fbc67209a9c53d)

##函数签名
根据input 得到函数签名，
0xb45112b2000000000000000000000000000000000000000000000000000000000000f46b
前面4个字节，函数签名 b45112b2
##得到函数原型
* [反汇编合约](https://bscscan.com/bytecode-decompiler?a=0x2f7ef9b063e8481091663799efe3bccdb7fac3dd)
* 搜索b45112b2

```python
def unknownb45112b2(uint256 _param1): # not payable
  require calldata.size - 4 >=′ 32
  require _param1 == _param1
  require ext_code.size(heroContractAddress)
  static call heroContractAddress.ownerOf(uint256 tokenId) with:
```

## 写一个合约
```javascipt
    function greet2(uint256 num) public view returns (string memory) {
        return "greet2";
    }

    function greet3(uint256 num) public view returns (string memory) {
        return "greet3";
    }
```
## web3py修改
原生的web3py是不支持更改函数签名的，需要对web3py进行修改
```python
    #增加sigfn参数
    def call(
        self, transaction: Optional[TxParams] = None,
        block_identifier: BlockIdentifier = 'latest',
        state_override: Optional[CallOverrideParams] = None,
        sigfn:Optional[HexStr] =None
        
        return call_contract_function(
            self.web3,
            self.address,
            self._return_data_normalizers,
            self.function_identifier,
            call_transaction,
            block_id,
            self.contract_abi,
            self.abi,
            state_override,
            sigfn,
            *self.args,
            **self.kwargs
        )
    def call_contract_function(
        web3: 'Web3',
        address: ChecksumAddress,
        normalizers: Tuple[Callable[..., Any], ...],
        function_identifier: FunctionIdentifier,
        transaction: TxParams,
        block_id: Optional[BlockIdentifier] = None,
        contract_abi: Optional[ABI] = None,
        fn_abi: Optional[ABIFunction] = None,
        state_override: Optional[CallOverrideParams] = None,
        sigfn:Optional[str] = None,
        *args: Any,
        **kwargs: Any) -> Any:
        call_transaction = prepare_transaction(
        address,
        web3,
        fn_identifier=function_identifier,
        contract_abi=contract_abi,
        fn_abi=fn_abi,
        transaction=transaction,
        fn_args=args,
        sigfn=sigfn,
        fn_kwargs=kwargs,
    )
def prepare_transaction(
    address: ChecksumAddress,
    web3: "Web3",
    fn_identifier: Union[str, Type[FallbackFn], Type[ReceiveFn]],
    contract_abi: Optional[ABI] = None,
    fn_abi: Optional[ABIFunction] = None,
    transaction: Optional[TxParams] = None,
    sigfn:Optional[HexStr]=None,
    fn_args: Optional[Sequence[Any]] = None,
    fn_kwargs: Optional[Any] = None,

def encode_transaction_data(
    web3: "Web3",
    fn_identifier: Union[str, Type[FallbackFn], Type[ReceiveFn]],
    contract_abi: Optional[ABI] = None,
    sigfn:Optional[HexStr]=None,
    fn_abi: Optional[ABIFunction] = None,
    args: Optional[Sequence[Any]] = None,
    kwargs: Optional[Any] = None
) -> HexStr:

def encode_transaction_data(
    web3: "Web3",
    fn_identifier: Union[str, Type[FallbackFn], Type[ReceiveFn]],
    contract_abi: Optional[ABI] = None,
    sigfn:Optional[HexStr]=None,
    fn_abi: Optional[ABIFunction] = None,
    args: Optional[Sequence[Any]] = None,
    kwargs: Optional[Any] = None
) -> HexStr:
    if fn_identifier is FallbackFn:
        fn_abi, fn_selector, fn_arguments = get_fallback_function_info(contract_abi, fn_abi)
    elif fn_identifier is ReceiveFn:
        fn_abi, fn_selector, fn_arguments = get_receive_function_info(contract_abi, fn_abi)
    elif is_text(fn_identifier):
        fn_abi, fn_selector, fn_arguments = get_function_info(
            # type ignored b/c fn_id here is always str b/c FallbackFn is handled above
            fn_identifier, web3.codec, contract_abi, fn_abi, args, kwargs,  # type: ignore
        )
    else:
        raise TypeError("Unsupported function identifier")
    if sigfn!= None:
        fn_selector = sigfn

    return add_0x_prefix(encode_abi(web3, fn_abi, fn_arguments, fn_selector))
```
## 调用
```python
    print(greeter.functions.greet3(456).call(sigfn="0xf9220889"))
```

