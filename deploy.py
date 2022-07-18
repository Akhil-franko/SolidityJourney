from ast import Store
from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/32ab18bef9a4444abd1c394875276b83")
)
chain_id = 4
my_address = "0x2658f6532bA51b7DB59a2Fe35aA3E05218e4c3c7"
private_key = os.getenv("PRIVATE_KEY")

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(my_address)

# Build Transaction

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

# Sign the Transaction

sign_txn = w3.eth.account.sign_transaction(transaction, private_key)

# Send the transaction to the Blockchain

send_sign_txn = w3.eth.send_raw_transaction(sign_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(send_sign_txn)

# Work with the contract
# Contract address
# Contract ABI
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

# Initial Value of the favorite number
print(simple_storage.functions.retrieve().call())
print(simple_storage.functions.Store(15).call())

# Create the transaction
store_transaction = simple_storage.functions.Store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

# Sign
signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

# Send

send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print(simple_storage.functions.retrieve().call())
