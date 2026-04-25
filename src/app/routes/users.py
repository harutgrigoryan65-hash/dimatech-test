from __future__ import annotations

from sanic import Blueprint, Request
from sanic.response import json
from sqlalchemy import select

from app.auth import auth_required
from app.models import Account, Payment, User
from app.responses import error
from app.security import create_access_token, verify_password
from app.serializers import account_to_dict, payment_to_dict, user_to_dict
from app.validators import require_json_object, required_str

users_bp = Blueprint("users", url_prefix="/users")


@users_bp.post("/login")
async def login(request: Request):
    try:
        data = require_json_object(request.json)
        email = required_str(data, "email").lower()
        password = required_str(data, "password")
    except ValueError as exc:
        return error(str(exc), status=422)

    user = await request.ctx.session.scalar(
        select(User).where(User.email == email, User.role == "user")
    )
    if user is None or not verify_password(password, user.password_hash):
        return error("Invalid email or password", status=401)

    return json({"access_token": create_access_token(user.id, user.role), "token_type": "bearer"})


@users_bp.get("/me")
@auth_required(role="user")
async def me(request: Request):
    return json(user_to_dict(request.ctx.current_user))


@users_bp.get("/me/accounts")
@auth_required(role="user")
async def my_accounts(request: Request):
    result = await request.ctx.session.scalars(
        select(Account).where(Account.user_id == request.ctx.current_user.id).order_by(Account.id)
    )
    return json({"items": [account_to_dict(account) for account in result.all()]})


@users_bp.get("/me/payments")
@auth_required(role="user")
async def my_payments(request: Request):
    result = await request.ctx.session.scalars(
        select(Payment)
        .where(Payment.user_id == request.ctx.current_user.id)
        .order_by(Payment.created_at.desc(), Payment.id.desc())
    )
    return json({"items": [payment_to_dict(payment) for payment in result.all()]})

