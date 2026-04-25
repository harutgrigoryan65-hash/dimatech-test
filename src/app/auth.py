from __future__ import annotations

from functools import wraps
from typing import Callable, ParamSpec, TypeVar

import jwt
from sanic import Request
from sqlalchemy import select

from app.models import User
from app.responses import error
from app.security import decode_access_token

P = ParamSpec("P")
R = TypeVar("R")


def auth_required(role: str | None = None):
    def decorator(handler: Callable[P, R]) -> Callable[P, R]:
        @wraps(handler)
        async def wrapper(request: Request, *args: P.args, **kwargs: P.kwargs):
            header = request.headers.get("Authorization", "")
            scheme, _, token = header.partition(" ")
            if scheme.lower() != "bearer" or not token:
                return error("Authorization bearer token is required", status=401)

            try:
                payload = decode_access_token(token)
                user_id = int(payload["sub"])
            except (jwt.PyJWTError, KeyError, ValueError):
                return error("Invalid or expired token", status=401)

            user = await request.ctx.session.scalar(select(User).where(User.id == user_id))
            if user is None:
                return error("User not found", status=401)
            if role is not None and user.role != role:
                return error("Forbidden", status=403)

            request.ctx.current_user = user
            return await handler(request, *args, **kwargs)

        return wrapper

    return decorator

