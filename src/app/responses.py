from __future__ import annotations

from decimal import Decimal
from typing import Any

from sanic.response import json


def error(message: str, status: int = 400, **extra: Any):
    return json({"error": message, **extra}, status=status)


def money(value: Decimal) -> str:
    return f"{value:.2f}"

