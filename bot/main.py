from __future__ import annotations

import asyncio

from aiogram import Bot, Dispatcher
from redis.asyncio import Redis

from bot.handlers import router
from config.settings import get_settings
from app.logging import configure_logging


async def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    bot = Bot(token=settings.telegram_bot_token)
    dp = Dispatcher()
    dp.include_router(router)

    redis = Redis.from_url(settings.redis_url)
    await redis.ping()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
