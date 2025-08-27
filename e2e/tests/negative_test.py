import time
import pytest
from requests.exceptions import HTTPError
from e2e.utils.test_helpers import get_balance, get_wallet_ids

def assert_error_response(exc_info, status_code, detail_substring):
    assert f"{status_code} Client Error" in str(exc_info.value)
    response_json = exc_info.value.response.json()
    assert detail_substring in response_json.get("detail", "")

@pytest.mark.parametrize(
    "from_currency,to_currency",
    [
        ("ETH", "TRX"),
        ("TRX", "ETH"),
    ]
)
def test_insufficient_funds(from_currency, to_currency, wallet_client, quote_client, token):
    from_wallet_id, to_wallet_id = get_wallet_ids(wallet_client, token, from_currency, to_currency)

    from_wallet_balance_before_convert = get_balance(wallet_client, token, from_wallet_id)
    amount = from_wallet_balance_before_convert + 1.0
    print(f"FROM wallet balance before: {from_wallet_balance_before_convert}, trying to convert: {amount}")

    with pytest.raises(HTTPError) as exc_info:
        quote_client.create_quote(token, from_currency, to_currency, from_wallet_id, to_wallet_id, amount)

    assert_error_response(exc_info, 412, f"Insufficient funds available in source wallet #{from_wallet_id}")


@pytest.mark.parametrize(
    "from_currency,to_currency,amount",
    [
        ("ETH", "TRX", 1),
    ]
)
def test_quote_expiry(from_currency, to_currency, amount, wallet_client, quote_client, token):
    from_wallet_id, to_wallet_id = get_wallet_ids(wallet_client, token, from_currency, to_currency)

    quote_response = quote_client.create_quote(token, from_currency, to_currency, from_wallet_id, to_wallet_id, amount)
    print(f"Quote created with uuid: {quote_response['uuid']}. Waiting for expiry...")

    time.sleep(21)

    with pytest.raises(HTTPError) as exc_info:
        quote_client.accept_quote(token, quote_response["uuid"])

    assert_error_response(exc_info, 412, "Precondition Failed")


@pytest.mark.parametrize(
    "from_currency,to_currency,amount",
    [
        ("ETH", "TRX", 0),
    ]
)
def test_zero_convert(from_currency, to_currency, amount, wallet_client, quote_client, token):
    from_wallet_id, to_wallet_id = get_wallet_ids(wallet_client, token, from_currency, to_currency)

    from_wallet_balance_before_convert = get_balance(wallet_client, token, from_wallet_id)
    print(f"FROM wallet balance before: {from_wallet_balance_before_convert}, trying to convert: {amount}")

    with pytest.raises(HTTPError) as exc_info:
        quote_client.create_quote(token, from_currency, to_currency, from_wallet_id, to_wallet_id, amount)

    assert_error_response(exc_info, 400, "One of 'amountIn' or 'amountOut' must be specified but not both.")


@pytest.mark.parametrize(
    "from_currency,to_currency",
    [
        ("ETH", "TRXY"),
        ("ABC", "TRX"),
    ]
)
def test_unsupported_currency(from_currency, to_currency, wallet_client, quote_client, token):
    with pytest.raises(ValueError) as exc_info:
        get_wallet_ids(wallet_client, token, from_currency, to_currency)

    assert "No wallet with currency" in str(exc_info.value)

