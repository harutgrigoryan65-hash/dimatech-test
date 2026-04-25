from __future__ import annotations

from collections.abc import AsyncIterator
from decimal import Decimal

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base
from app.models import Account, User
from app.security import hash_password


@pytest_asyncio.fixture
async def session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with session_factory() as db_session:
        db_session.add_all(
            [
                User(
                    id=1,
                    email="user@example.com",
                    full_name="Test User",
                    password_hash=hash_password("user12345", b"default-user-salt"),
                    role="user",
                ),
                User(
                    id=2,
                    email="other@example.com",
                    full_name="Other User",
                    password_hash=hash_password("other12345", b"default-other-salt"),
                    role="user",
                ),
                User(
                    id=3,
                    email="admin@example.com",
                    full_name="Test Admin",
                    password_hash=hash_password("admin12345", b"default-admin-salt"),
                    role="admin",
                ),
                Account(id=1, user_id=1, balance=Decimal("0.00")),
                Account(id=2, user_id=2, balance=Decimal("5.00")),
            ]
        )
        await db_session.commit()
        yield db_session

    await engine.dispose()

