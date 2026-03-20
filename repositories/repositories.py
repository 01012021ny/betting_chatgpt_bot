from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.entities import Digest, Event, Recommendation, Subscription, User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def upsert_user(self, telegram_id: int, username: str | None, timezone_str: str = "UTC") -> User:
        result = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if user is None:
            user = User(telegram_id=telegram_id, username=username, timezone=timezone_str)
            self.session.add(user)
            await self.session.flush()
        return user

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()


class SubscriptionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def subscribe(self, user_id: int) -> Subscription:
        subscription = Subscription(user_id=user_id, is_active=True)
        self.session.add(subscription)
        await self.session.flush()
        return subscription

    async def unsubscribe(self, user_id: int) -> None:
        result = await self.session.execute(select(Subscription).where(Subscription.user_id == user_id))
        subscription = result.scalar_one_or_none()
        if subscription:
            subscription.is_active = False

    async def active_user_ids(self) -> list[int]:
        result = await self.session.execute(select(Subscription.user_id).where(Subscription.is_active.is_(True)))
        return list(result.scalars().all())


class EventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_events(self, events: list[Event]) -> None:
        for event in events:
            self.session.add(event)

    async def get_upcoming(self, sports: list[str], limit_per_sport: int) -> list[Event]:
        now = datetime.now(timezone.utc)
        result = await self.session.execute(
            select(Event)
            .where(Event.status == "prematch", Event.sport.in_(sports), Event.starts_at_utc >= now)
            .order_by(Event.starts_at_utc.asc())
        )
        grouped: dict[str, list[Event]] = {sport: [] for sport in sports}
        for event in result.scalars().all():
            if len(grouped[event.sport]) < limit_per_sport:
                grouped[event.sport].append(event)
        merged: list[Event] = []
        for sport in sports:
            merged.extend(grouped[sport])
        return merged


class RecommendationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_recommendation(
        self,
        event_id: int,
        market_type: str,
        recommendation: str,
        odds: float,
        explanation: str,
        confidence: float,
        risk: str,
    ) -> Recommendation:
        rec = Recommendation(
            event_id=event_id,
            market_type=market_type,
            recommendation=recommendation,
            odds=odds,
            explanation=explanation,
            confidence=confidence,
            risk=risk,
        )
        self.session.add(rec)
        await self.session.flush()
        return rec


class DigestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_digest(self, digest_type: str, content: str, scheduled_for_utc: datetime) -> Digest:
        digest = Digest(digest_type=digest_type, content=content, scheduled_for_utc=scheduled_for_utc)
        self.session.add(digest)
        await self.session.flush()
        return digest
