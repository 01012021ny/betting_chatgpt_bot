from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class EventDTO:
    provider_event_id: str
    sport: str
    tournament: str
    home_team: str
    away_team: str
    starts_at_utc: datetime


@dataclass(slots=True)
class OddsDTO:
    event_provider_id: str
    market_type: str
    selection: str
    odds: float


@dataclass(slots=True)
class RecommendationDTO:
    market_type: str
    recommendation: str
    odds: float
    explanation: str
    confidence: float
    risk: str
