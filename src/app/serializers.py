from __future__ import annotations

from app.models import Account, Payment, User
from app.responses import money


def user_to_dict(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
    }


def admin_user_to_dict(user: User) -> dict:
    return {
        **user_to_dict(user),
        "role": user.role,
        "accounts": [account_to_dict(account) for account in user.accounts],
    }


def account_to_dict(account: Account) -> dict:
    return {
        "id": account.id,
        "user_id": account.user_id,
        "balance": money(account.balance),
    }


def payment_to_dict(payment: Payment) -> dict:
    return {
        "id": payment.id,
        "transaction_id": payment.transaction_id,
        "user_id": payment.user_id,
        "account_id": payment.account_id,
        "amount": money(payment.amount),
        "created_at": payment.created_at.isoformat() if payment.created_at else None,
    }

