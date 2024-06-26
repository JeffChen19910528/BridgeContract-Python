from web3 import Web3
import json
import time

#取得所有的區塊鏈上智能合約位置
def get_all_contracts():
    # 获取最新区块号
    latest_block_number = web3.eth.block_number
    print("Latest block number:", latest_block_number)

    # 遍历每个区块
    for block_number in range(latest_block_number + 1):
        # 获取区块
        block = web3.eth.get_block(block_number)

        # 检查区块中的每笔交易
        for tx_hash in block.transactions:
            # 获取交易详情
            tx = web3.eth.get_transaction(tx_hash)

            # 检查交易是否为合约创建交易
            if tx.to is None and tx.input:
                # 获取合约地址
                contract_address = web3.eth.get_transaction_receipt(tx_hash).contractAddress
                print("Contract created at block {}, address: {}".format(block_number, contract_address))

#取得區塊鏈上所有的交易希哈值
def get_all_transaction_hashes():
    # 获取最新区块号
    latest_block_number = web3.eth.block_number
    print("Latest block number:", latest_block_number)
    tx_hashs =[]
    # 遍历每个区块
    for block_number in range(latest_block_number + 1):
        # 获取区块
        block = web3.eth.get_block(block_number)

        # 获取区块中的交易哈希值
        for tx_hash in block.transactions:
            print("Transaction Hash:", tx_hash.hex())
            tx_hashs.append(tx_hash.hex())
    
    return tx_hashs


def get_transaction_receipt(tx_hash):
    # 获取交易收据
    receipt = web3.eth.get_transaction_receipt(tx_hash)
    return receipt

# 获取区块链上的所有用户钱包地址
def get_all_wallet_addresses():
    # 存放地址的集合
    addresses = set()

    # 获取最新区块号
    latest_block_number = web3.eth.block_number
    print("Latest block number:", latest_block_number)

    # 遍历每个区块
    for block_number in range(latest_block_number + 1):
        # 获取区块
        block = web3.eth.get_block(block_number)

        # 获取区块中的交易
        for tx_hash in block.transactions:
            # 获取交易详情
            tx = web3.eth.get_transaction(tx_hash)
            
            # 添加发送者和接收者地址到集合中
            if tx['from']:
                addresses.add(tx['from'])
            if tx['to']:
                addresses.add(tx['to'])

    return addresses

# 获取区块链的 TPS
def get_blockchain_tps(interval=10):
    start_block_number = web3.eth.block_number

    while True:
        start_time = time.time()
        start_block = web3.eth.block_number

        # 等待一段时间
        time.sleep(interval)

        end_time = time.time()
        end_block = web3.eth.block_number

        # 计算 TPS
        block_count = end_block - start_block
        elapsed_time = end_time - start_time
        tps = block_count / elapsed_time if elapsed_time > 0 else 0

        print("TPS for last {} seconds: {:.2f}".format(interval, tps))


with open('IP.txt', 'r') as file:
    # 读取每一行并存储在一个列表中
    lines = file.readlines()

for line in lines:
    print(line.strip()) 
    # Prive Chain web3 instance
    web3 = Web3(Web3.HTTPProvider('http://'+line.strip()+':8545'))



if web3.is_connected():
    print('blockchin netowork is connected!')
    get_all_contracts()
    tx_hashs = get_all_transaction_hashes()
    for tx_hash in tx_hashs:
        receipt = get_transaction_receipt(tx_hash)
        if receipt:
            print(tx_hash+":")
            print("Transaction Receipt:")
            print("Status:", receipt['status'])
            print("Gas Used:", receipt['gasUsed'])
            print("Contract Address:", receipt['contractAddress'])  # 如果是合约创建交易，会有合约地址
            print("Logs:", receipt['logs'])
            print("")
        else:
            print("Transaction receipt not found.")

    # 打印区块链上的所有用户钱包地址
    wallet_addresses = get_all_wallet_addresses()
    print("All Wallet Addresses:")
    for address in wallet_addresses:
        print(address)

    #get_blockchain_tps()
else:
    print('blockchin netowork is not found!')

