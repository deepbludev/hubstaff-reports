from datetime import datetime
from functools import lru_cache
from typing import Any, Callable, Coroutine, cast

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger


class Scheduler:
    """A generic scheduler that can register and manage multiple jobs."""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self._jobs: dict[str, dict[str, Any]] = {}

    def register(
        self,
        job: Callable[..., Coroutine[Any, Any, None]],
        cron: str,
        job_id: str,
        name: str | None = None,
    ) -> None:
        """
        Register a new job with the scheduler.

        Args:
            job: The async job to run
            cron: Cron expression in format "HH:MM"
            job_id: Unique identifier for the job
            name: Optional name for the job
        """
        time = datetime.strptime(cron, "%H:%M").time()
        self._jobs[job_id] = {
            "job": job,
            "cron": cron,
            "name": name or job_id,
        }

        self.scheduler.add_job(
            job,
            trigger=CronTrigger(hour=time.hour, minute=time.minute),
            id=job_id,
            name=name or job_id,
            replace_existing=True,
        )
        logger.info(f"Registered job '{job_id}' to run at {cron}")

    def get_scheduled_jobs(self) -> list[Job]:
        """Get the scheduled jobs."""
        return cast(list[Job], self.scheduler.get_jobs())

    def remove_job(self, job_id: str) -> None:
        """
        Remove a job from the scheduler.

        Args:
            job_id: The ID of the job to remove
        """
        if job_id in self._jobs:
            self.scheduler.remove_job(job_id)
            del self._jobs[job_id]
            logger.info(f"Removed job '{job_id}' from scheduler")

    def start(self) -> None:
        """Start the scheduler."""
        self.scheduler.start()
        logger.info("Job scheduler started")

    def shutdown(self) -> None:
        """Stop the scheduler."""
        self.scheduler.shutdown()
        logger.info("Job scheduler stopped")


@lru_cache
def get_scheduler() -> Scheduler:
    """Get the global scheduler instance."""

    return Scheduler()
