from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_type = db.Column(db.String(64), nullable=False)
    transaction_id = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(64))
    reason = db.Column(db.String(64))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    debtor_name = db.Column(db.String(128), nullable=False)
    debtor_account = db.Column(db.String(34), nullable=False)
    creditor_name = db.Column(db.String(128), nullable=False)
    creditor_account = db.Column(db.String(34), nullable=False)
    remittance_info = db.Column(db.Text)
    mandate_id = db.Column(db.String(128))
    iso20022_data = db.Column(db.Text, nullable=False)
    ethereum_data = db.Column(db.Text, nullable=False)
    transaction_hash = db.Column(db.String(66), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    
    # New fields for additional message types
    original_message_id = db.Column(db.String(128))
    original_message_type = db.Column(db.String(64))
    group_status = db.Column(db.String(64))
    requested_execution_date = db.Column(db.Date)
    requested_collection_date = db.Column(db.Date)
    return_reason = db.Column(db.String(64))
    case_id = db.Column(db.String(128))
    creator = db.Column(db.String(128))
    account_id = db.Column(db.String(34))
    statement_id = db.Column(db.String(128))
    creation_date_time = db.Column(db.DateTime)
    balance = db.Column(db.Numeric(10, 2))

    # New fields for bank and ACH responses
    bank_response = db.Column(db.Text)
    ach_response = db.Column(db.Text)
