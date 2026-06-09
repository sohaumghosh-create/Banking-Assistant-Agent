from tools.banking_tools import (
    get_account_balance,
    get_recent_transactions,
    get_upcoming_payments
)

AVAILABLE_TOOLS = {
    "get_account_balance": get_account_balance,
    "get_recent_transactions": get_recent_transactions,
    "get_upcoming_payments": get_upcoming_payments
}