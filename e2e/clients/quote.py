import requests
from e2e.config import BVNK_SIMULATOR_HOST

class QuoteClient:
    BASE_PATH = "/api/v1/quote"

    def __init__(self, api_host: str = BVNK_SIMULATOR_HOST):
        self.api_host = api_host.rstrip("/")
        self.base_url = f"{self.api_host}{self.BASE_PATH}"

    def _get_headers(self, token):
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def create_quote(self, token, from_currency, to_currency, from_wallet, to_wallet, amount_in):
        url = self.base_url
        headers = self._get_headers(token)
        body = {
            "from": from_currency,
            "to": to_currency,
            "fromWallet": from_wallet,
            "useMaximum": True,
            "useMinimum": True,
            "reference": "Test",
            "toWallet": to_wallet,
            "amountOut": 0,
            "amountIn": amount_in,
            "payInMethod": "",
            "payOutMethod": ""
        }
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def accept_quote(self, token, uuid):
        url = f"{self.base_url}/accept/{uuid}"
        headers = self._get_headers(token)
        response = requests.put(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_quote(self, token, uuid):
        url = f"{self.base_url}/{uuid}"
        headers = self._get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()