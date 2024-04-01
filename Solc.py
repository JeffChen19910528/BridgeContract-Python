import solcx
from solcx import compile_standard
from web3 import Web3
from web3.middleware import geth_poa_middleware

# 安装solc并设置版本
solcx.install_solc(version='0.8.25')
solcx.set_solc_version('0.8.25')

with open('IP.txt', 'r') as file:
    # 读取每一行并存储在一个列表中
    lines = file.readlines()

# 设置以太坊节点的地址
for line in lines:
    print(line.strip()) 
    # Prive Chain web3 instance
    w3 = Web3(Web3.HTTPProvider('http://'+line.strip()+':8545'))

# 添加POA中间件（如果你的节点是POA网络）
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# 从文本文件中读取合约源代码
contract_source_file = "SimpleStorage.sol"  # 替换为你的合约文件名

with open(contract_source_file, "r") as file:
    contract_source_code = file.read()

# 编译合约
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {contract_source_file: {"content": contract_source_code}},
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "evm.bytecode"]
            }
        }
    }
})

# 获取合约字节码
bytecode = compiled_sol['contracts'][contract_source_file]['SimpleStorage']['evm']['bytecode']['object']

# 获取ABI
abi = compiled_sol['contracts'][contract_source_file]['SimpleStorage']['abi']

# 创建合约对象
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# 设置默认账户
w3.eth.default_account = w3.eth.accounts[0]  # 替换为你的账户地址
w3.geth.personal.unlock_account(w3.eth.accounts[0], '123456')

# 部署合约
tx_hash = SimpleStorage.constructor().transact({'from': w3.eth.default_account, 'gas': 2000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# 获取部署的合约地址
contract_address = tx_receipt.contractAddress

print("Contract deployed at address:", contract_address)