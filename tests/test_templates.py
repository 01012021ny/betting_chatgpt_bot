from __future__ import annotations

from datetime import datetime, timezone

from models.entities import Event, Recommendation
from templates.digest_templates import render_regular_digest


def test_regular_digest_contains_disclaimer() -> None:
    event = Event(
        id=1,
        provider_event_id="m1",
        sport="football",
        tournament="EPL",
        home_team="Team A",
        away_team="Team B",
        starts_at_utc=datetime(2026, 3, 18, 15, 0, tzinfo=timezone.utc),
        status="prematch",
    )
    rec = Recommendation(
        id=1,
        event_id=1,
        market_type="moneyline",
        recommendation="Team A Win",
        odds=1.8,
        explanation="Форма лучше.",
        confidence=0.71,
        risk="medium",
    )

    text = render_regular_digest([(event, [rec])], "UTC")

    assert "информационный характер" in text
    assert "Team A vs Team B" in text
