from __future__ import annotations

from datetime import datetime, timedelta, timezone
import random

from models.schemas import EventDTO, OddsDTO
from providers.interfaces import EventsProvider, OddsProvider


class MockEventsProvider(EventsProvider):
    async def get_upcoming_events(self, starts_after: datetime, starts_before: datetime) -> list[EventDTO]:
        sports = ["football", "hockey", "tennis", "basketball", "mma"]
        tournaments = {
            "football": "UEFA Champions League",
            "hockey": "NHL",
            "tennis": "ATP Tour",
            "basketball": "NBA",
            "mma": "UFC",
        }
        now = datetime.now(timezone.utc)
        events: list[EventDTO] = []
        for idx in range(1, 41):
            sport = sports[idx % len(sports)]
            start_at = now + timedelta(minutes=30 * idx)
            if starts_after <= start_at <= starts_before:
                events.append(
                    EventDTO(
                        provider_event_id=f"mock-{idx}",
                        sport=sport,
                        tournament=tournaments[sport],
                        home_team=f"{sport.capitalize()} Team {idx}",
                        away_team=f"{sport.capitalize()} Team {idx + 1}",
                        starts_at_utc=start_at,
                    )
                )
        return events


class MockOddsProvider(OddsProvider):
    async def get_prematch_odds(self, provider_event_ids: list[str]) -> list[OddsDTO]:
        markets = ["moneyline", "total_over_under", "handicap"]
        odds: list[OddsDTO] = []
        for event_id in provider_event_ids:
            for market in markets:
                odd = round(random.uniform(1.35, 3.3), 2)
                selection = "Home Win" if market == "moneyline" else "Over 2.5"
                odds.append(
                    OddsDTO(
                        event_provider_id=event_id,
                        market_type=market,
                        selection=selection,
                        odds=odd,
                    )
                )
        return odds
