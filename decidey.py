from bank_api_integration import get_bank_api
from ethereum_integration import translate_to_ethereum, store_on_blockchain
import logging

logger = logging.getLogger(__name__)

def process_transaction(parsed_data, bank_name):
    try:
        bank_api = get_bank_api(bank_name)
        bank_response = bank_api.send_transaction(parsed_data)
        
        if bank_response.get("status") == "error":
            logger.error(f"Error from bank API: {bank_response.get('message')}")
            return {
                'bank_response': bank_response,
                'ethereum_data': None,
                'transaction_hash': None
            }
        
        ethereum_data = translate_to_ethereum(parsed_data)
        transaction_hash = store_on_blockchain(ethereum_data)
        
        return {
            'bank_response': bank_response,
            'ethereum_data': ethereum_data,
            'transaction_hash': transaction_hash
        }
    except Exception as e:
        logger.error(f"Error in process_transaction: {str(e)}")
        return {
            'bank_response': {'status': 'error', 'message': str(e)},
            'ethereum_data': None,
            'transaction_hash': None
        }
