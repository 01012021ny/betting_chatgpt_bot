from __future__ import annotations

from config.settings import Settings
from models.schemas import OddsDTO
from services.recommendation_engine import RuleBasedRecommendationEngine


def test_engine_filters_by_odds_and_confidence() -> None:
    settings = Settings(min_odds=1.4, max_odds=2.2, confidence_threshold=0.6)
    engine = RuleBasedRecommendationEngine(settings=settings)

    odds = [
        OddsDTO(event_provider_id="e1", market_type="moneyline", selection="Home Win", odds=1.55),
        OddsDTO(event_provider_id="e1", market_type="handicap", selection="-1", odds=2.9),
    ]

    recs = engine.build_recommendations(odds, max_per_event=2)
    assert "e1" in recs
    assert len(recs["e1"]) == 1
    assert recs["e1"][0].risk in {"low", "medium", "high"}
