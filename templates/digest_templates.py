from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

from models.entities import Event, Recommendation

DISCLAIMER = "Прогноз носит информационный характер. Ставки связаны с риском. 18+"


def _fmt_dt(dt_utc: datetime, tz_name: str) -> str:
    return dt_utc.astimezone(ZoneInfo(tz_name)).strftime("%Y-%m-%d %H:%M %Z")


def render_regular_digest(rows: list[tuple[Event, list[Recommendation]]], tz_name: str) -> str:
    grouped: dict[str, list[tuple[Event, list[Recommendation]]]] = defaultdict(list)
    for event, recs in rows:
        grouped[event.sport].append((event, recs))

    lines = ["📊 Дневная сводка по ставкам"]
    for sport, items in grouped.items():
        lines.append(f"\n🏷️ {sport.title()}")
        for event, recs in items:
            lines.append(
                f"• {event.tournament}: {event.home_team} vs {event.away_team} | {_fmt_dt(event.starts_at_utc, tz_name)}"
            )
            if recs:
                rec = recs[0]
                lines.append(
                    f"  Рекомендация: {rec.recommendation} ({rec.market_type}), кэф ~{rec.odds}, "
                    f"уверенность {rec.confidence:.0%}, риск {rec.risk}."
                )
                lines.append(f"  Почему: {rec.explanation}")

    lines.append(f"\n⚠️ {DISCLAIMER}")
    return "\n".join(lines)


def render_evening_digest(rows: list[tuple[Event, list[Recommendation]]], tz_name: str) -> str:
    grouped: dict[str, list[tuple[Event, list[Recommendation]]]] = defaultdict(list)
    for event, recs in rows:
        grouped[event.sport].append((event, recs))

    lines = ["🌆 Вечерняя топ-сводка"]
    for sport, items in grouped.items():
        lines.append(f"\n🏆 {sport.title()} — топ события")
        for event, recs in items:
            lines.append(
                f"• {event.tournament}: {event.home_team} vs {event.away_team} | {_fmt_dt(event.starts_at_utc, tz_name)}"
            )
            for idx, rec in enumerate(recs[:2], start=1):
                lines.append(
                    f"  {idx}) {rec.market_type}: {rec.recommendation}, кэф ~{rec.odds}, "
                    f"уверенность {rec.confidence:.0%}, риск {rec.risk}."
                )
                lines.append(f"     Почему: {rec.explanation}")

    lines.append(f"\n⚠️ {DISCLAIMER}")
    return "\n".join(lines)
