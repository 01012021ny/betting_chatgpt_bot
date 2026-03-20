from __future__ import annotations

import asyncio

from models.base import Base
from models import entities  # noqa: F401
from repositories.db import engine


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
