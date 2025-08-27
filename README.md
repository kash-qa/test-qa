# Test-QA: E2E API Testing Project

## Overview

This project provides end-to-end (E2E) automated tests for the BVNK Simulator API, focusing on wallet and quote operations such as currency conversion, balance checks, and error handling.

## Features

- **Automated E2E tests** for wallet and quote API endpoints
- **Negative tests** for error scenarios (insufficient funds, expired quotes, unsupported currencies, etc.)
- **Reusable fixtures** for API clients, authentication tokens, and wallet IDs
- **Test parametrization** to easily run the same test logic with different currencies and amounts
- **Helper utilities** for common actions (fetching balances, wallet IDs, waiting for payment status)
- **Custom assertion helpers** for validating error responses

## Usage

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Run all tests:**
    ```bash
    python3 -m pytest e2e/tests/
    ```

3. **Generate an HTML report (example report attached):**
    ```bash
    python3 -m pytest --html=report.html
    ```

## Key Concepts

### Fixtures

Fixtures are used to set up and provide reusable components for tests, such as API clients and authentication tokens.  
They are defined in `conftest.py` and injected into test functions as arguments:

```python
@pytest.fixture
def wallet_client():
    return WalletClient()

@pytest.fixture
def token(setup_client):
    init = setup_client.init_account()
    return init["access_token"]
```

### Parametrization

Tests use `pytest.mark.parametrize` to run the same logic with different input data, improving coverage and reducing code duplication:

```python
@pytest.mark.parametrize(
    "from_currency,to_currency,amount",
    [
        ("ETH", "TRX", 1),
        ("TRX", "USDT", 420),
        ("TRX", "ETH", 987),
    ]
)
def test_convert_currency(from_currency, to_currency, amount, wallet_client, quote_client, token):
    ...
```


### Helper Utilities

Common actions like fetching wallet balances or IDs are extracted to helper functions in `utils/test_helpers.py` for reuse and clarity.


### Example of the run in VSCode
<img width="805" height="88" alt="image" src="https://github.com/user-attachments/assets/019a8721-92eb-4f7d-849c-e17428a2a4b9" />
<img width="797" height="13" alt="image" src="https://github.com/user-attachments/assets/e6da2014-3430-4789-9602-461c374e87c2" />


