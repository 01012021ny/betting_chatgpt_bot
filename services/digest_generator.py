from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import Settings
from models.entities import Event
from providers.interfaces import EventsProvider, OddsProvider
from repositories.repositories import DigestRepository, EventRepository, RecommendationRepository
from services.cache import CacheService
from services.recommendation_engine import RuleBasedRecommendationEngine
from templates.digest_templates import render_evening_digest, render_regular_digest

logger = structlog.get_logger(__name__)


@dataclass(slots=True)
class DigestGeneratorService:
    settings: Settings
    events_provider: EventsProvider
    odds_provider: OddsProvider
    cache_service: CacheService
    recommendation_engine: RuleBasedRecommendationEngine

    async def generate_digest(
        self,
        session: AsyncSession,
        digest_type: str,
        scheduled_for_utc: datetime,
        user_timezone: str = "UTC",
    ) -> str:
        starts_after = datetime.now(timezone.utc)
        starts_before = starts_after + timedelta(hours=self.settings.upcoming_window_hours)

        events_dto = await self.events_provider.get_upcoming_events(starts_after, starts_before)

        # Store fetched payload in cache for fallback.
        await self.cache_service.set_json(
            "events:last_success",
            {
                "events": [
                    {
                        "provider_event_id": e.provider_event_id,
                        "sport": e.sport,
                        "tournament": e.tournament,
                        "home_team": e.home_team,
                        "away_team": e.away_team,
                        "starts_at_utc": e.starts_at_utc.isoformat(),
                    }
                    for e in events_dto
                ]
            },
            ttl_seconds=900,
        )

        event_models = [
            Event(
                provider_event_id=e.provider_event_id,
                sport=e.sport,
                tournament=e.tournament,
                home_team=e.home_team,
                away_team=e.away_team,
                starts_at_utc=e.starts_at_utc,
                status="prematch",
            )
            for e in events_dto
            if e.sport in self.settings.enabled_sports
        ]

        event_repo = EventRepository(session)
        await event_repo.save_events(event_models)

        provider_ids = [e.provider_event_id for e in event_models]
        odds = await self.odds_provider.get_prematch_odds(provider_ids)

        max_per_event = 2 if digest_type == "evening" else 1
        rec_map = self.recommendation_engine.build_recommendations(odds, max_per_event=max_per_event)

        rec_repo = RecommendationRepository(session)
        rows: list[tuple[Event, list]] = []

        for event in event_models:
            recs = rec_map.get(event.provider_event_id, [])
            saved_recs = []
            for rec in recs:
                saved = await rec_repo.save_recommendation(
                    event_id=event.id,
                    market_type=rec.market_type,
                    recommendation=rec.recommendation,
                    odds=rec.odds,
                    explanation=rec.explanation,
                    confidence=rec.confidence,
                    risk=rec.risk,
                )
                saved_recs.append(saved)
            if saved_recs:
                rows.append((event, saved_recs))

        if digest_type == "evening":
            content = render_evening_digest(rows, user_timezone)
        else:
            content = render_regular_digest(rows, user_timezone)

        digest_repo = DigestRepository(session)
        await digest_repo.save_digest(digest_type, content, scheduled_for_utc)

        logger.info("digest_generated", digest_type=digest_type, items=len(rows))
        return content
