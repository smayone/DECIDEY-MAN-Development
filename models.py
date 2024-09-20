from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iso20022_data = db.Column(db.Text, nullable=False)
    ethereum_data = db.Column(db.Text, nullable=False)
    transaction_hash = db.Column(db.String(66), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
