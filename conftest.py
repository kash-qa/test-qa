import pytest
from e2e.clients.setup import SetupClient
from e2e.clients.wallet import WalletClient
from e2e.clients.quote import QuoteClient

@pytest.fixture
def setup_client():
    return SetupClient()

@pytest.fixture
def wallet_client():
    return WalletClient()

@pytest.fixture
def quote_client():
    return QuoteClient()

@pytest.fixture
def token(setup_client):
    init = setup_client.init_account()
    return init["access_token"]