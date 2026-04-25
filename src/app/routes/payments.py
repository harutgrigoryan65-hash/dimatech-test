from __future__ import annotations

from sanic import Blueprint, Request
from sanic.response import json

from app.services.payments import process_payment_webhook

payments_bp = Blueprint("payments", url_prefix="/payments")


@payments_bp.post("/webhook")
async def webhook(request: Request):
    body, status = await process_payment_webhook(request.ctx.session, request.json)
    return json(body, status=status)
