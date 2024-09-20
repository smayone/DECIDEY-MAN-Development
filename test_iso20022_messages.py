import requests
import json

BASE_URL = "http://localhost:5000"

def send_iso20022_message(message_type, xml_data):
    url = f"{BASE_URL}/api/transaction"
    payload = json.dumps({"iso20022_data": xml_data})
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=payload)
    print(f"Response for {message_type}:")
    print(response.json())
    print("---")

# Test payment status report
payment_status_report = """
<Document>
  <FIToFIPmtStsRpt>
    <TxInfAndSts>
      <OrgnlTxId>TX123456</OrgnlTxId>
      <TxSts>ACCP</TxSts>
      <StsRsnInf>
        <Rsn>
          <Cd>AC01</Cd>
        </Rsn>
      </StsRsnInf>
      <OrgnlTxRef>
        <Amt>
          <InstdAmt Ccy="EUR">100.00</InstdAmt>
        </Amt>
        <Dbtr>
          <Nm>John Doe</Nm>
        </Dbtr>
        <DbtrAcct>
          <Id>
            <IBAN>DE89370400440532013000</IBAN>
          </Id>
        </DbtrAcct>
        <Cdtr>
          <Nm>Jane Smith</Nm>
        </Cdtr>
        <CdtrAcct>
          <Id>
            <IBAN>FR7630006000011234567890189</IBAN>
          </Id>
        </CdtrAcct>
      </OrgnlTxRef>
    </TxInfAndSts>
  </FIToFIPmtStsRpt>
</Document>
"""

# Test credit transfer
credit_transfer = """
<Document>
  <FIToFICstmrCdtTrf>
    <CdtTrfTxInf>
      <PmtId>
        <EndToEndId>E2E12345</EndToEndId>
      </PmtId>
      <IntrBkSttlmAmt Ccy="USD">500.00</IntrBkSttlmAmt>
      <Dbtr>
        <Nm>Alice Johnson</Nm>
      </Dbtr>
      <DbtrAcct>
        <Id>
          <IBAN>GB29NWBK60161331926819</IBAN>
        </Id>
      </DbtrAcct>
      <Cdtr>
        <Nm>Bob Williams</Nm>
      </Cdtr>
      <CdtrAcct>
        <Id>
          <IBAN>ES9121000418450200051332</IBAN>
        </Id>
      </CdtrAcct>
      <RmtInf>
        <Ustrd>Invoice payment</Ustrd>
      </RmtInf>
    </CdtTrfTxInf>
  </FIToFICstmrCdtTrf>
</Document>
"""

# Test direct debit
direct_debit = """
<Document>
  <FIToFICstmrDrctDbt>
    <DrctDbtTxInf>
      <PmtId>
        <EndToEndId>DD987654</EndToEndId>
      </PmtId>
      <IntrBkSttlmAmt Ccy="GBP">75.50</IntrBkSttlmAmt>
      <DrctDbtTx>
        <MndtRltdInf>
          <MndtId>MD2023001</MndtId>
        </MndtRltdInf>
      </DrctDbtTx>
      <Dbtr>
        <Nm>Charlie Brown</Nm>
      </Dbtr>
      <DbtrAcct>
        <Id>
          <IBAN>IT60X0542811101000000123456</IBAN>
        </Id>
      </DbtrAcct>
      <Cdtr>
        <Nm>Energy Company</Nm>
      </Cdtr>
      <CdtrAcct>
        <Id>
          <IBAN>NL91ABNA0417164300</IBAN>
        </Id>
      </CdtrAcct>
    </DrctDbtTxInf>
  </FIToFICstmrDrctDbt>
</Document>
"""

# Test payment return
payment_return = """
<Document>
  <PmtRtr>
    <TxInf>
      <RtrId>RTN123456</RtrId>
      <OrgnlTxId>ORGTX789012</OrgnlTxId>
      <RtrdIntrBkSttlmAmt Ccy="EUR">200.00</RtrdIntrBkSttlmAmt>
      <RtrRsnInf>
        <Rsn>
          <Cd>AC04</Cd>
        </Rsn>
      </RtrRsnInf>
    </TxInf>
  </PmtRtr>
</Document>
"""

# Test resolution of investigation
resolution_of_investigation = """
<Document>
  <RsltnOfInvstgtn>
    <CaseAssgnmt>
      <Id>CASE2023001</Id>
      <Cretr>
        <Pty>
          <Nm>Bank XYZ</Nm>
        </Pty>
      </Cretr>
    </CaseAssgnmt>
    <Sts>
      <Conf>RSLV</Conf>
    </Sts>
  </RsltnOfInvstgtn>
</Document>
"""

# Test bank to customer statement
bank_to_customer_statement = """
<Document>
  <BkToCstmrStmt>
    <Stmt>
      <Id>STMT2023001</Id>
      <CreDtTm>2023-09-20T10:00:00</CreDtTm>
      <Acct>
        <Id>
          <IBAN>CH9300762011623852957</IBAN>
        </Id>
      </Acct>
      <Bal>
        <Amt Ccy="CHF">1000.00</Amt>
      </Bal>
    </Stmt>
  </BkToCstmrStmt>
</Document>
"""

if __name__ == "__main__":
    send_iso20022_message("Payment Status Report", payment_status_report)
    send_iso20022_message("Credit Transfer", credit_transfer)
    send_iso20022_message("Direct Debit", direct_debit)
    send_iso20022_message("Payment Return", payment_return)
    send_iso20022_message("Resolution of Investigation", resolution_of_investigation)
    send_iso20022_message("Bank to Customer Statement", bank_to_customer_statement)
