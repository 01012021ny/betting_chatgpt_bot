from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from services.delivery_service import DeliveryService
from services.digest_generator import DigestGeneratorService

logger = structlog.get_logger(__name__)


@dataclass(slots=True)
class DigestJobRunner:
    digest_service: DigestGeneratorService
    delivery_service: DeliveryService

    async def run(self, session: AsyncSession, digest_type: str, subscribers: list[tuple[int, str]]) -> None:
        scheduled_for_utc = datetime.now(timezone.utc)
        for telegram_id, tz_name in subscribers:
            digest_text = await self.digest_service.generate_digest(
                session=session,
                digest_type=digest_type,
                scheduled_for_utc=scheduled_for_utc,
                user_timezone=tz_name,
            )
            await self.delivery_service.send_with_retry(telegram_id, digest_text)
        logger.info("job_finished", digest_type=digest_type, subscribers=len(subscribers))
