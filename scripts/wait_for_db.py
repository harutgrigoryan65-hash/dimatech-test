from __future__ import annotations

import asyncio
import os

import asyncpg


def asyncpg_url(url: str) -> str:
    return url.replace("postgresql+asyncpg://", "postgresql://", 1)


async def main() -> None:
    database_url = asyncpg_url(
        os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://postgres:postgres@localhost:5432/test_pythonmid",
        )
    )
    last_error: Exception | None = None
    for _ in range(30):
        try:
            connection = await asyncpg.connect(database_url)
            await connection.close()
            return
        except Exception as exc:
            last_error = exc
            await asyncio.sleep(1)
    raise RuntimeError(f"Database is not available: {last_error}")


if __name__ == "__main__":
    asyncio.run(main())

