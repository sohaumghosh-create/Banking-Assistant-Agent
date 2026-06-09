from data.mock_db import BANK_DATABASE

def get_account_balance(account_id: str) -> dict:
    account = BANK_DATABASE.get(account_id)
    if not account:
        return {"error": "Account not found"}
    return account["balances"]

def get_recent_transactions(account_id: str, count: int = 10) -> list:
    account = BANK_DATABASE.get(account_id)
    if not account:
        return [{"error": "Account not found"}]
    return account["transactions"][:count]

def get_upcoming_payments(account_id: str) -> list:
    account = BANK_DATABASE.get(account_id)
    if not account:
        return [{"error": "Account not found"}]
    return account["upcoming_payments"]