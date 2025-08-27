import pytest
import math
from e2e.utils.test_helpers import wait_for_payment_success, get_balance, get_wallet_ids

@pytest.mark.parametrize(
    "from_currency,to_currency,amount",
    [
        ("ETH", "TRX", 1),
        ("TRX", "USDT", 420),
        ("TRX", "ETH", 987),
    ]
)
def test_convert_currency(from_currency, to_currency, amount, wallet_client, quote_client, token):
    from_wallet_id, to_wallet_id = get_wallet_ids(wallet_client, token, from_currency, to_currency)

    from_wallet_balance_before_convert = get_balance(wallet_client, token, from_wallet_id)
    to_wallet_balance_before_convert = get_balance(wallet_client, token, to_wallet_id)
    print ("FROM wallet balance before:", from_wallet_balance_before_convert, "TO wallet balance before:", to_wallet_balance_before_convert)

    quote_response = quote_client.create_quote(token, from_currency, to_currency, from_wallet_id, to_wallet_id, amount)
    quote_client.accept_quote(token, quote_response["uuid"])

    wait_for_payment_success(quote_client, token, quote_response["uuid"])
    print("Payment status reached SUCCESS.")

    from_wallet_balance_after_convert = get_balance(wallet_client, token, from_wallet_id)
    deducted_value = from_wallet_balance_before_convert - from_wallet_balance_after_convert
    print("Expected FROM wallet balance difference:", amount, "Actual balance:", deducted_value)

    assert deducted_value == amount, (
    f"Expected {amount} to be deducted from {from_currency} wallet (id {from_wallet_id}), "
    f"but got {deducted_value} (before: {from_wallet_balance_before_convert}, after: {from_wallet_balance_after_convert})"
)
    
    to_wallet_balance_after_convert = get_balance(wallet_client, token, to_wallet_id)
    converted_amount = to_wallet_balance_after_convert - to_wallet_balance_before_convert
    print("Actual converted amount:", converted_amount, "Expected amount:", quote_response["amountOut"])

    assert math.isclose(converted_amount, float(quote_response["amountOut"]), rel_tol=1e-6), \
        f"Expected converted amount {quote_response['amountOut']}, got {converted_amount}"