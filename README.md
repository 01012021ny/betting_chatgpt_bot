# Betting Telegram Digest Bot

Production-ready каркас Telegram-бота для ежедневных спортивных сводок с рекомендациями по ставкам.

## Что реализовано

- Модульная архитектура: `bot/`, `services/`, `providers/`, `scheduler/`, `repositories/`, `models/`, `config/`, `tests/`.
- Scheduler на APScheduler с расписанием 09:00, 12:00, 15:00, 18:00, 20:00 (UTC).
- Provider layer: интерфейсы + mock providers (`events provider`, `odds provider`).
- Rule-based recommendation engine, заменяемый в будущем на ML/LLM.
- Digest generator с разными форматами для дневной и вечерней сводки.
- PostgreSQL модели (SQLAlchemy).
- Redis cache service и точка для fallback.
- Telegram handlers: `/start`, `/help`, `/subscribe`, `/unsubscribe`, `/settings`, `/today`, `/top`, `/status`.
- Retry отправки в Telegram (`tenacity`) и structured logging (`structlog`).

## Архитектура (high-level)

1. **Scheduler** запускает задачи по UTC-расписанию.
2. **Digest generator** получает prematch-события и коэффициенты через provider layer.
3. **Recommendation engine** считает confidence/risk и отбирает рекомендации по конфигу.
4. **Template renderer** формирует текст сводки + обязательный дисклеймер.
5. **Delivery service** рассылает подписчикам с retry и логами.
6. Все сущности и результаты сохраняются в PostgreSQL; кеш и очереди — через Redis.

## Быстрый старт

```bash
cp .env.example .env
docker compose up --build
```

## Локальный запуск без Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python -m bot.main
```

## Тесты

```bash
pytest
```

## Пример обычной сводки (09:00/12:00/15:00/18:00)

```text
📊 Дневная сводка по ставкам

🏷️ Football
• UEFA Champions League: Arsenal vs Napoli | 2026-03-18 18:00 MSK
  Рекомендация: Home Win (moneyline), кэф ~1.82, уверенность 74%, риск medium.
  Почему: Rule-based оценка: коэффициент в допустимом диапазоне, маркет ликвидный, событие prematch.

🏷️ Hockey
• NHL: Rangers vs Bruins | 2026-03-18 19:00 MSK
  Рекомендация: Over 5.5 (total_over_under), кэф ~1.91, уверенность 71%, риск medium.
  Почему: Rule-based оценка: коэффициент в допустимом диапазоне, маркет ликвидный, событие prematch.

⚠️ Прогноз носит информационный характер. Ставки связаны с риском. 18+
```

## Пример вечерней сводки (20:00)

```text
🌆 Вечерняя топ-сводка

🏆 Football — топ события
• UEFA Champions League: Real Madrid vs Inter | 2026-03-18 22:00 MSK
  1) moneyline: Home Win, кэф ~1.76, уверенность 76%, риск low.
     Почему: Rule-based оценка: коэффициент в допустимом диапазоне, маркет ликвидный, событие prematch.
  2) handicap: Home -1, кэф ~2.15, уверенность 66%, риск medium.
     Почему: Rule-based оценка: коэффициент в допустимом диапазоне, маркет ликвидный, событие prematch.

⚠️ Прогноз носит информационный характер. Ставки связаны с риском. 18+
```

## Масштабирование

- Добавить Celery/RQ workers поверх Redis для горизонтального масштабирования доставки.
- Подключить реальный Odds API через реализацию `providers.interfaces`.
- Вынести ML/LLM engine в отдельный сервис и включить feature flag.
