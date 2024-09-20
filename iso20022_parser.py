import xmltodict

def parse_iso20022(xml_data):
    """
    Parse ISO20022 XML data and extract relevant information.
    """
    parsed_data = xmltodict.parse(xml_data)
    
    # Extract relevant information from the parsed data
    # This is a simplified example, adjust according to the actual ISO20022 structure
    transaction = parsed_data['Document']['FIToFIPmtStsRpt']['TxInfAndSts']
    
    return {
        'transaction_id': transaction['OrgnlTxId'],
        'amount': transaction['OrgnlTxRef']['Amt']['InstdAmt']['#text'],
        'currency': transaction['OrgnlTxRef']['Amt']['InstdAmt']['@Ccy'],
        'debtor': transaction['OrgnlTxRef']['Dbtr']['Nm'],
        'creditor': transaction['OrgnlTxRef']['Cdtr']['Nm'],
        'status': transaction['TxSts'],
    }
