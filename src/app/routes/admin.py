from __future__ import annotations

from sanic import Blueprint, Request
from sanic.response import json
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.auth import auth_required
from app.models import User
from app.responses import error
from app.security import create_access_token, hash_password, verify_password
from app.serializers import admin_user_to_dict, user_to_dict
from app.validators import optional_str, require_json_object, required_str

admin_bp = Blueprint("admin", url_prefix="/admin")


@admin_bp.post("/login")
async def login(request: Request):
    try:
        data = require_json_object(request.json)
        email = required_str(data, "email").lower()
        password = required_str(data, "password")
    except ValueError as exc:
        return error(str(exc), status=422)

    admin = await request.ctx.session.scalar(
        select(User).where(User.email == email, User.role == "admin")
    )
    if admin is None or not verify_password(password, admin.password_hash):
        return error("Invalid email or password", status=401)

    return json({"access_token": create_access_token(admin.id, admin.role), "token_type": "bearer"})


@admin_bp.get("/me")
@auth_required(role="admin")
async def me(request: Request):
    return json(user_to_dict(request.ctx.current_user))


@admin_bp.get("/users")
@auth_required(role="admin")
async def list_users(request: Request):
    result = await request.ctx.session.scalars(
        select(User)
        .where(User.role == "user")
        .options(selectinload(User.accounts))
        .order_by(User.id)
    )
    return json({"items": [admin_user_to_dict(user) for user in result.all()]})


@admin_bp.post("/users")
@auth_required(role="admin")
async def create_user(request: Request):
    try:
        data = require_json_object(request.json)
        email = required_str(data, "email").lower()
        full_name = required_str(data, "full_name")
        password = required_str(data, "password")
    except ValueError as exc:
        return error(str(exc), status=422)

    user = User(email=email, full_name=full_name, password_hash=hash_password(password), role="user")
    request.ctx.session.add(user)
    try:
        await request.ctx.session.commit()
    except IntegrityError:
        await request.ctx.session.rollback()
        return error("User with this email already exists", status=409)

    return json(user_to_dict(user), status=201)


@admin_bp.patch("/users/<user_id:int>")
@auth_required(role="admin")
async def update_user(request: Request, user_id: int):
    try:
        data = require_json_object(request.json)
        email = optional_str(data, "email")
        full_name = optional_str(data, "full_name")
        password = optional_str(data, "password")
    except ValueError as exc:
        return error(str(exc), status=422)

    user = await request.ctx.session.scalar(select(User).where(User.id == user_id, User.role == "user"))
    if user is None:
        return error("User not found", status=404)

    if email is not None:
        user.email = email.lower()
    if full_name is not None:
        user.full_name = full_name
    if password is not None:
        user.password_hash = hash_password(password)

    try:
        await request.ctx.session.commit()
    except IntegrityError:
        await request.ctx.session.rollback()
        return error("User with this email already exists", status=409)

    return json(user_to_dict(user))


@admin_bp.delete("/users/<user_id:int>")
@auth_required(role="admin")
async def delete_user(request: Request, user_id: int):
    user = await request.ctx.session.scalar(select(User).where(User.id == user_id, User.role == "user"))
    if user is None:
        return error("User not found", status=404)

    await request.ctx.session.delete(user)
    await request.ctx.session.commit()
    return json({"status": "deleted"})

