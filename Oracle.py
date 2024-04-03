from web3 import Web3

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
        if tx['to'] is None:
            deployed_contracts.append(tx['contractAddress'])
            
            # 獲取合約的交易日誌記錄
            receipt = web3.eth.get_transaction_receipt(tx.hash)
            for log in receipt.logs:
                print(f"      Log: {log}")

# 獲取所有帳戶地址和餘額
accounts = web3.eth.accounts
for account in accounts:
    balance = web3.eth.get_balance(account)
    print(f"Account {account}: {web3.from_wei(balance, 'ether')} ETH")