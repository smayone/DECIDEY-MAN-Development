from web3 import Web3
from config import Config

w3 = Web3(Web3.HTTPProvider(Config.ETHEREUM_NODE_URL))

def translate_to_ethereum(parsed_data):
    """
    Translate parsed ISO20022 data to Ethereum-compatible format.
    """
    return {
        'transaction_id': w3.keccak(text=parsed_data['transaction_id']).hex(),
        'amount': w3.to_wei(parsed_data['amount'], 'ether'),
        'currency': w3.keccak(text=parsed_data['currency']).hex(),
        'debtor': w3.keccak(text=parsed_data['debtor']).hex(),
        'creditor': w3.keccak(text=parsed_data['creditor']).hex(),
        'status': w3.keccak(text=parsed_data['status']).hex(),
    }

def store_on_blockchain(ethereum_data):
    """
    Store the Ethereum-compatible data on the blockchain using a smart contract.
    """
    # In a real-world scenario, you would deploy the smart contract and interact with it here
    # For this example, we'll just return a dummy transaction hash
    return w3.keccak(text=str(ethereum_data)).hex()
