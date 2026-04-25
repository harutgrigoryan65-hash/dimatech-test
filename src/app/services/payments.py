from __future__ import annotations

from decimal import Decimal
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Account, Payment, User
from app.security import verify_payment_signature
from app.validators import require_json_object, required_amount, required_int, required_str


def parse_payment_webhook(data: Any) -> tuple[str, int, int, Decimal]:
    payload = require_json_object(data)
    transaction_id = required_str(payload, "transaction_id")
    user_id = required_int(payload, "user_id")
    account_id = required_int(payload, "account_id")
    amount = required_amount(payload, "amount")
    return transaction_id, user_id, account_id, amount


async def process_payment_webhook(session: AsyncSession, data: Any) -> tuple[dict[str, Any], int]:
    try:
        transaction_id, user_id, account_id, amount = parse_payment_webhook(data)
    except ValueError as exc:
        return {"error": str(exc)}, 422

    if not verify_payment_signature(data):
        return {"error": "Invalid signature"}, 403

    try:
        async with session.begin():
            existing_payment = await session.scalar(
                select(Payment).where(Payment.transaction_id == transaction_id)
            )
            if existing_payment is not None:
                return {"status": "already_processed", "payment_id": existing_payment.id}, 200

            user = await session.scalar(select(User).where(User.id == user_id, User.role == "user"))
            if user is None:
                return {"error": "User not found"}, 404

            account = await session.scalar(
                select(Account).where(Account.id == account_id).with_for_update()
            )
            if account is None:
                account = Account(id=account_id, user_id=user_id)
                session.add(account)
                await session.flush()
            elif account.user_id != user_id:
                return {"error": "Account does not belong to user"}, 409

            payment = Payment(
                transaction_id=transaction_id,
                user_id=user_id,
                account_id=account_id,
                amount=amount,
            )
            session.add(payment)
            account.balance += amount
            await session.flush()
    except IntegrityError:
        return {"status": "already_processed"}, 200

    return {
        "status": "processed",
        "transaction_id": transaction_id,
        "account_id": account_id,
        "amount": f"{amount:.2f}",
    }, 201

