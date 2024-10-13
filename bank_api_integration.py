import requests
from abc import ABC, abstractmethod
from config import Config

class BankAPI(ABC):
    @abstractmethod
    def send_transaction(self, transaction_data):
        pass

    @abstractmethod
    def get_transaction_status(self, transaction_id):
        pass

class ACHSystem(ABC):
    @abstractmethod
    def process_ach_transaction(self, ach_data):
        pass

    @abstractmethod
    def get_ach_status(self, ach_id):
        pass

class ExampleBankAPI(BankAPI):
    def __init__(self):
        self.api_key = Config.EXAMPLE_BANK_API_KEY
        self.base_url = Config.EXAMPLE_BANK_BASE_URL

    def send_transaction(self, transaction_data):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(f"{self.base_url}/transactions", json=transaction_data, headers=headers)
        return response.json()

    def get_transaction_status(self, transaction_id):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(f"{self.base_url}/transactions/{transaction_id}", headers=headers)
        return response.json()

class AnotherBankAPI(BankAPI):
    def __init__(self):
        self.api_key = Config.ANOTHER_BANK_API_KEY
        self.base_url = Config.ANOTHER_BANK_BASE_URL

    def send_transaction(self, transaction_data):
        headers = {"X-API-Key": self.api_key}
        response = requests.post(f"{self.base_url}/api/v1/transactions", json=transaction_data, headers=headers)
        return response.json()

    def get_transaction_status(self, transaction_id):
        headers = {"X-API-Key": self.api_key}
        response = requests.get(f"{self.base_url}/api/v1/transactions/{transaction_id}", headers=headers)
        return response.json()

class ExampleACHSystem(ACHSystem):
    def __init__(self):
        self.ach_api_key = Config.EXAMPLE_ACH_API_KEY
        self.ach_base_url = Config.EXAMPLE_ACH_BASE_URL

    def process_ach_transaction(self, ach_data):
        headers = {"Authorization": f"Bearer {self.ach_api_key}"}
        response = requests.post(f"{self.ach_base_url}/ach", json=ach_data, headers=headers)
        return response.json()

    def get_ach_status(self, ach_id):
        headers = {"Authorization": f"Bearer {self.ach_api_key}"}
        response = requests.get(f"{self.ach_base_url}/ach/{ach_id}", headers=headers)
        return response.json()

class AnotherACHSystem(ACHSystem):
    def __init__(self):
        self.ach_api_key = Config.ANOTHER_ACH_API_KEY
        self.ach_base_url = Config.ANOTHER_ACH_BASE_URL

    def process_ach_transaction(self, ach_data):
        headers = {"X-ACH-API-Key": self.ach_api_key}
        response = requests.post(f"{self.ach_base_url}/v2/ach-transactions", json=ach_data, headers=headers)
        return response.json()

    def get_ach_status(self, ach_id):
        headers = {"X-ACH-API-Key": self.ach_api_key}
        response = requests.get(f"{self.ach_base_url}/v2/ach-transactions/{ach_id}", headers=headers)
        return response.json()

def get_bank_api(bank_name):
    if bank_name == "example_bank":
        return ExampleBankAPI()
    elif bank_name == "another_bank":
        return AnotherBankAPI()
    else:
        raise ValueError(f"Unsupported bank: {bank_name}")

def get_ach_system(ach_name):
    if ach_name == "example_ach":
        return ExampleACHSystem()
    elif ach_name == "another_ach":
        return AnotherACHSystem()
    else:
        raise ValueError(f"Unsupported ACH system: {ach_name}")
