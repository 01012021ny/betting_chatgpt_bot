from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


def build_scheduler() -> AsyncIOScheduler:
    return AsyncIOScheduler(timezone="UTC")


def add_digest_jobs(scheduler: AsyncIOScheduler, job_func) -> None:  # type: ignore[no-untyped-def]
    for hour in (9, 12, 15, 18):
        scheduler.add_job(job_func, CronTrigger(hour=hour, minute=0), kwargs={"digest_type": "regular"})
    scheduler.add_job(job_func, CronTrigger(hour=20, minute=0), kwargs={"digest_type": "evening"})
