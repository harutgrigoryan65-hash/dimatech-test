from __future__ import annotations

from sanic import Blueprint

from app.routes.admin import admin_bp
from app.routes.payments import payments_bp
from app.routes.users import users_bp


api = Blueprint.group(users_bp, admin_bp, payments_bp, url_prefix="/api")

