from web3 import Web3
import time

# 連接到私有區塊鏈節點
with open('IP.txt', 'r') as file:
    # 读取每一行并存储在一个列表中
    lines = file.readlines()

for line in lines:
    print(line.strip()) 
    # Prive Chain web3 instance
    infura_url = "http://"+line.strip()+":8545" # 更改為您的私有節點URL

web3 = Web3(Web3.HTTPProvider(infura_url))

# 獲取最新區塊號碼
latest_block = web3.eth.get_block('latest')
print(f"Latest block number: {latest_block.number}")


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


# 遍歷所有區塊並獲取交易和挖礦詳細信息
deployed_contracts = []
for block_number in range(latest_block.number, 0, -1):
    block = web3.eth.get_block(block_number, full_transactions=True)
    print(f"Block {block_number}:")
    print(f"  Miner: {block.miner}")
    print(f"  Transactions: {len(block.transactions)}")
    for tx in block.transactions:
        print(f"    Transaction hash: {tx.hash.hex()}")
        print(f"      From: {tx['from']}")
        print(f"      To: {tx['to']}")
        print(f"      Value: {web3.from_wei(tx['value'], 'ether')} ETH")
        
       # 檢查是否為合約部署交易
        if isinstance(tx, dict) and 'contractAddress' in tx:
             deployed_contract_address = tx['contractAddress']
             deployed_contracts.append(deployed_contract_address)
             print(f" Deployed contract address: {deployed_contract_address}")
            
        # 獲取合約的交易日誌記錄
        receipt = web3.eth.get_transaction_receipt(tx.hash)
        for log in receipt.logs:
            print(f"      Log: {log}")

# 獲取所有帳戶地址和餘額
accounts = web3.eth.accounts
for account in accounts:
    balance = web3.eth.get_balance(account)
    print(f"Account {account}: {web3.from_wei(balance, 'ether')} ETH")

get_all_contracts()

# 獲取初始帳號地址列表
initial_accounts = web3.eth.accounts

# 設置區塊過濾器
block_filter = web3.eth.filter('latest')

# 持續監控新的區塊
while True:
    for event in block_filter.get_new_entries():
        block = web3.eth.get_block(event, full_transactions=True)
        print(f"Block {block.number}:")
        print(f" Miner: {block.miner}")
        print(f" Transactions: {len(block.transactions)}")

        for tx in block.transactions:
            print(f" Transaction hash: {tx.hash.hex()}")
            print(f" From: {tx['from']}")
            print(f" To: {tx['to']}")
            print(f" Value: {web3.from_wei(tx['value'], 'ether')} ETH")

             # 檢查是否為合約部署交易
            if isinstance(tx, dict) and 'contractAddress' in tx:
                deployed_contract_address = tx['contractAddress']
                deployed_contracts.append(deployed_contract_address)
                print(f" Deployed contract address: {deployed_contract_address}")

            # 獲取合約的交易日誌記錄
            receipt = web3.eth.get_transaction_receipt(tx.hash)
            for log in receipt.logs:
                print(f" Log: {log}")

    # 獲取當前所有帳號地址列表
    current_accounts = web3.eth.accounts

    # 檢查是否有新的帳號地址產生
    new_accounts = list(set(current_accounts) - set(initial_accounts))
    if new_accounts:
        print(f"New accounts detected: {', '.join(new_accounts)}")
        initial_accounts = current_accounts  

    # 每 5 秒查詢一次新的區塊
    time.sleep(5)