from __future__ import annotations

from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Account, Payment
from app.security import build_payment_signature
from app.services.payments import process_payment_webhook


def signed_payload(**overrides):
    signature = overrides.pop("signature", None)
    payload = {
        "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
        "user_id": 1,
        "account_id": 1,
        "amount": 100,
    }
    payload.update(overrides)
    payload["signature"] = signature or build_payment_signature(payload)
    return payload


@pytest.mark.asyncio
async def test_process_payment_increases_balance_and_saves_transaction(session: AsyncSession) -> None:
    body, status = await process_payment_webhook(session, signed_payload())

    account = await session.get(Account, 1)
    payment = await session.scalar(
        select(Payment).where(Payment.transaction_id == "5eae174f-7cd0-472c-bd36-35660f00132b")
    )

    assert status == 201
    assert body["status"] == "processed"
    assert account is not None
    assert account.balance == Decimal("100.00")
    assert payment is not None
    assert payment.amount == Decimal("100.00")


@pytest.mark.asyncio
async def test_process_payment_is_idempotent_by_transaction_id(session: AsyncSession) -> None:
    payload = signed_payload()

    first_body, first_status = await process_payment_webhook(session, payload)
    second_body, second_status = await process_payment_webhook(session, payload)

    account = await session.get(Account, 1)
    payments = (await session.scalars(select(Payment))).all()

    assert first_status == 201
    assert first_body["status"] == "processed"
    assert second_status == 200
    assert second_body["status"] == "already_processed"
    assert account is not None
    assert account.balance == Decimal("100.00")
    assert len(payments) == 1


@pytest.mark.asyncio
async def test_process_payment_creates_missing_user_account(session: AsyncSession) -> None:
    body, status = await process_payment_webhook(
        session,
        signed_payload(
            transaction_id="8d3a1f82-4a91-4aac-bd28-75f79e24e0e5",
            account_id=10,
            amount=25,
        ),
    )

    account = await session.get(Account, 10)

    assert status == 201
    assert body["status"] == "processed"
    assert account is not None
    assert account.user_id == 1
    assert account.balance == Decimal("25.00")


@pytest.mark.asyncio
async def test_process_payment_rejects_invalid_signature(session: AsyncSession) -> None:
    payload = signed_payload(signature="broken")

    body, status = await process_payment_webhook(session, payload)

    assert status == 403
    assert body == {"error": "Invalid signature"}


@pytest.mark.asyncio
async def test_process_payment_rejects_foreign_account(session: AsyncSession) -> None:
    body, status = await process_payment_webhook(
        session,
        signed_payload(
            transaction_id="0a669956-cc1f-4ddc-9e98-cfe417a3ad92",
            account_id=2,
            amount=25,
        ),
    )

    account = await session.get(Account, 2)

    assert status == 409
    assert body == {"error": "Account does not belong to user"}
    assert account is not None
    assert account.balance == Decimal("5.00")
