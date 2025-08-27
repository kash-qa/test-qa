
import requests
from e2e.config import BVNK_SIMULATOR_HOST

class WalletClient:
    BASE_PATH = "/api/wallet"

    def __init__(self, api_host: str = BVNK_SIMULATOR_HOST):
        self.api_host = api_host.rstrip("/")
        self.base_url = f"{self.api_host}{self.BASE_PATH}"

    def _get_headers(self, token):
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def list_wallets(self, token):
        url = self.base_url
        headers = self._get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_wallet(self, token, wallet_id):
        url = f"{self.base_url}/{wallet_id}"
        headers = self._get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_wallet_id_by_currency(self, token, code):
        wallets = self.list_wallets(token)
        wallet = next((w for w in wallets if w.get("currency", {}).get("code") == code), None)
        if not wallet:
            raise ValueError(f"No wallet with currency '{code}' found")
        return wallet["id"]
