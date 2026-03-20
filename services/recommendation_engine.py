from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from config.settings import Settings
from models.schemas import OddsDTO, RecommendationDTO


RiskLevel = Literal["low", "medium", "high"]


@dataclass(slots=True)
class RuleBasedRecommendationEngine:
    settings: Settings

    def build_recommendations(self, odds: list[OddsDTO], max_per_event: int) -> dict[str, list[RecommendationDTO]]:
        by_event: dict[str, list[RecommendationDTO]] = {}

        for odd in odds:
            if not (self.settings.min_odds <= odd.odds <= self.settings.max_odds):
                continue

            confidence = self._confidence_by_odds(odd.odds)
            if confidence < self.settings.confidence_threshold:
                continue

            rec = RecommendationDTO(
                market_type=odd.market_type,
                recommendation=odd.selection,
                odds=odd.odds,
                explanation=(
                    "Rule-based оценка: коэффициент в допустимом диапазоне, "
                    "маркет ликвидный, событие prematch."
                ),
                confidence=confidence,
                risk=self._risk_label(confidence),
            )
            by_event.setdefault(odd.event_provider_id, []).append(rec)

        for event_id in by_event:
            by_event[event_id] = sorted(by_event[event_id], key=lambda x: x.confidence, reverse=True)[:max_per_event]

        return by_event

    @staticmethod
    def _confidence_by_odds(odds: float) -> float:
        # Простая эвристика: ниже коэффициент -> выше надежность.
        score = max(0.3, min(0.95, 1.05 - (odds - 1.2) * 0.25))
        return round(score, 2)

    @staticmethod
    def _risk_label(confidence: float) -> RiskLevel:
        if confidence >= 0.78:
            return "low"
        if confidence >= 0.62:
            return "medium"
        return "high"
