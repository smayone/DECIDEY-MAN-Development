import xmltodict
from typing import Dict, Any

def parse_iso20022(xml_data: str) -> Dict[str, Any]:
    """
    Parse ISO20022 XML data and extract relevant information.
    """
    parsed_data = xmltodict.parse(xml_data)
    
    # Determine the message type
    root_element = list(parsed_data['Document'].keys())[0]
    
    if root_element == 'FIToFIPmtStsRpt':
        return parse_payment_status_report(parsed_data['Document']['FIToFIPmtStsRpt'])
    elif root_element == 'FIToFICstmrCdtTrf':
        return parse_credit_transfer(parsed_data['Document']['FIToFICstmrCdtTrf'])
    elif root_element == 'FIToFICstmrDrctDbt':
        return parse_direct_debit(parsed_data['Document']['FIToFICstmrDrctDbt'])
    else:
        raise ValueError(f"Unsupported message type: {root_element}")

def parse_payment_status_report(data: Dict[str, Any]) -> Dict[str, Any]:
    transaction = data['TxInfAndSts']
    return {
        'message_type': 'payment_status_report',
        'transaction_id': transaction['OrgnlTxId'],
        'status': transaction['TxSts'],
        'reason': transaction.get('StsRsnInf', {}).get('Rsn', {}).get('Cd'),
        'amount': transaction['OrgnlTxRef']['Amt']['InstdAmt']['#text'],
        'currency': transaction['OrgnlTxRef']['Amt']['InstdAmt']['@Ccy'],
        'debtor_name': transaction['OrgnlTxRef']['Dbtr']['Nm'],
        'debtor_account': transaction['OrgnlTxRef']['DbtrAcct']['Id']['IBAN'],
        'creditor_name': transaction['OrgnlTxRef']['Cdtr']['Nm'],
        'creditor_account': transaction['OrgnlTxRef']['CdtrAcct']['Id']['IBAN'],
    }

def parse_credit_transfer(data: Dict[str, Any]) -> Dict[str, Any]:
    credit_transfer_info = data['CdtTrfTxInf']
    return {
        'message_type': 'credit_transfer',
        'transaction_id': credit_transfer_info['PmtId']['EndToEndId'],
        'amount': credit_transfer_info['IntrBkSttlmAmt']['#text'],
        'currency': credit_transfer_info['IntrBkSttlmAmt']['@Ccy'],
        'debtor_name': credit_transfer_info['Dbtr']['Nm'],
        'debtor_account': credit_transfer_info['DbtrAcct']['Id']['IBAN'],
        'creditor_name': credit_transfer_info['Cdtr']['Nm'],
        'creditor_account': credit_transfer_info['CdtrAcct']['Id']['IBAN'],
        'remittance_info': credit_transfer_info.get('RmtInf', {}).get('Ustrd'),
    }

def parse_direct_debit(data: Dict[str, Any]) -> Dict[str, Any]:
    direct_debit_info = data['DrctDbtTxInf']
    return {
        'message_type': 'direct_debit',
        'transaction_id': direct_debit_info['PmtId']['EndToEndId'],
        'amount': direct_debit_info['IntrBkSttlmAmt']['#text'],
        'currency': direct_debit_info['IntrBkSttlmAmt']['@Ccy'],
        'debtor_name': direct_debit_info['Dbtr']['Nm'],
        'debtor_account': direct_debit_info['DbtrAcct']['Id']['IBAN'],
        'creditor_name': direct_debit_info['Cdtr']['Nm'],
        'creditor_account': direct_debit_info['CdtrAcct']['Id']['IBAN'],
        'mandate_id': direct_debit_info['DrctDbtTx']['MndtRltdInf']['MndtId'],
    }
