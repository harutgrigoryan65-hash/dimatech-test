from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any


def require_json_object(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("JSON object is required")
    return data


def required_str(data: dict[str, Any], field: str) -> str:
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} is required")
    return value.strip()


def optional_str(data: dict[str, Any], field: str) -> str | None:
    value = data.get(field)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def required_int(data: dict[str, Any], field: str) -> int:
    value = data.get(field)
    if isinstance(value, bool):
        raise ValueError(f"{field} must be an integer")
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field} must be an integer") from None


def required_amount(data: dict[str, Any], field: str = "amount") -> Decimal:
    value = data.get(field)
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"{field} must be a number") from None
    if amount <= 0:
        raise ValueError(f"{field} must be greater than zero")
    return amount.quantize(Decimal("0.01"))

