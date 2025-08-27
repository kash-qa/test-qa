import requests
from e2e.config import BVNK_SIMULATOR_HOST

class SetupClient:
    def __init__(self, api_host=BVNK_SIMULATOR_HOST):
        self.api_host = api_host.rstrip("/")

    def init_account(self):
        url = f"{self.api_host}/init"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
