from web3 import Web3
import json

class Contract:
    def __init__(self, web3, accounts):
        self.web3 = web3
        self.accounts = accounts

    def get_contract(self):
        tx_hash = self.web3.eth.send_transaction({
            'from': self.accounts[0],
            'to': self.accounts[1],
            'value': self.web3.to_wei(1, 'ether'),
            'gas': 21000
        })
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        print(receipt)

class Password:
    def __init__(self, path):
        self.path = path

    def get_passwords(self):
        try:
            with open(self.path, 'r') as file:
                passwords = file.readlines()
                return [pwd.strip() for pwd in passwords]
        except IOError:
            print("Error: File does not appear to exist.")
            return []

# 連接到私有區塊鏈節點
with open('IP.txt', 'r') as file:
    # 读取每一行并存储在一个列表中
    lines = file.readlines()

for line in lines:
    print(line.strip()) 
    # Prive Chain web3 instance
    infura_url = "http://"+line.strip()+":8545" # 更改為您的私有節點URL

web3 = Web3(Web3.HTTPProvider(infura_url))

if web3.is_connected():
    print("Connection Successful")
else:
    print("Connection Failed")

print('block_number: ' + str(web3.eth.block_number))
accounts = web3.eth.accounts
print('accounts: ' + str(accounts))
print('account balance: ' + str(web3.eth.get_balance(accounts[0])))

password_handler = Password('password.txt')
passwords = password_handler.get_passwords()

for account, password in zip(accounts, passwords):
    try:
        web3.geth.personal.unlock_account(account, password, 15000)
    except Exception as e:
        print(f"Error unlocking account {account}: {str(e)}")

contract = Contract(web3, accounts)
contract.get_contract()

count = 0
for account in accounts:
    print('account balance'+ str(count) +': ' + str(web3.eth.get_balance(account)))
    count += 1