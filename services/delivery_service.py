from __future__ import annotations

import structlog
from aiogram import Bot
from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential

logger = structlog.get_logger(__name__)


class DeliveryService:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def send_with_retry(self, telegram_id: int, text: str) -> None:
        async for attempt in AsyncRetrying(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10), reraise=True):
            with attempt:
                await self.bot.send_message(chat_id=telegram_id, text=text)
                logger.info("delivery_success", telegram_id=telegram_id, attempt=attempt.retry_state.attempt_number)
