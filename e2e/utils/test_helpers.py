import time

def wait_for_payment_success(quote_client, token, uuid, max_retries=10, interval=2):
    for attempt in range(max_retries):
        quote_status = quote_client.get_quote(token, uuid)
        if quote_status["paymentStatus"] == "SUCCESS":
            return quote_status
        time.sleep(interval)
    raise TimeoutError(f"paymentStatus did not become SUCCESS after {max_retries} attempts")

def get_balance(wallet_client, token, wallet_id):
    return float(wallet_client.get_wallet(token, wallet_id)["balance"])

def get_wallet_ids(wallet_client, token, from_currency, to_currency):
    from_wallet_id = wallet_client.get_wallet_id_by_currency(token, from_currency)
    to_wallet_id = wallet_client.get_wallet_id_by_currency(token, to_currency)
    return from_wallet_id, to_wallet_id

def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Cannot convert {value} to float")