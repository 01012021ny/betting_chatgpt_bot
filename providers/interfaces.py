from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from models.schemas import EventDTO, OddsDTO


class EventsProvider(ABC):
    @abstractmethod
    async def get_upcoming_events(self, starts_after: datetime, starts_before: datetime) -> list[EventDTO]:
        raise NotImplementedError


class OddsProvider(ABC):
    @abstractmethod
    async def get_prematch_odds(self, provider_event_ids: list[str]) -> list[OddsDTO]:
        raise NotImplementedError
