import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ETHEREUM_NODE_URL = os.environ.get('ETHEREUM_NODE_URL', 'https://mainnet.infura.io/v3/YOUR-PROJECT-ID')
