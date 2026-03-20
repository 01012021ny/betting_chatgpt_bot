from __future__ import annotations

import json
from typing import Any

from redis.asyncio import Redis


class CacheService:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def get_json(self, key: str) -> dict[str, Any] | None:
        raw = await self.redis.get(key)
        if not raw:
            return None
        return json.loads(raw)

    async def set_json(self, key: str, value: dict[str, Any], ttl_seconds: int = 600) -> None:
        await self.redis.set(key, json.dumps(value), ex=ttl_seconds)
