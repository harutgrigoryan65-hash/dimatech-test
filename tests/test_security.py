from __future__ import annotations

import jwt

from app.security import (
    build_payment_signature,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_payment_signature_matches_task_example() -> None:
    payload = {
        "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
        "user_id": 1,
        "account_id": 1,
        "amount": 100,
    }

    assert (
        build_payment_signature(payload, secret_key="gfdmhghif38yrf9ew0jkf32")
        == "7b47e41efe564a062029da3367bde8844bea0fb049f894687cee5d57f2858bc8"
    )


def test_password_hash_roundtrip() -> None:
    password_hash = hash_password("secret", salt=b"stable-test-salt")

    assert verify_password("secret", password_hash)
    assert not verify_password("wrong", password_hash)


def test_access_token_roundtrip() -> None:
    token = create_access_token(user_id=42, role="admin")

    payload = decode_access_token(token)

    assert payload["sub"] == "42"
    assert payload["role"] == "admin"


def test_invalid_access_token_is_rejected() -> None:
    try:
        decode_access_token("not-a-token")
    except jwt.PyJWTError:
        return

    raise AssertionError("Invalid token was accepted")

