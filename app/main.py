from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.reports.jobs import register_report_jobs

from .api import reports_router
from .core.scheduler import get_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles the lifespan of the FastAPI app.
    """
    await startup(app)
    yield
    await shutdown(app)


app = FastAPI(lifespan=lifespan)
app.include_router(reports_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "OK"}


async def startup(app: FastAPI):
    """
    Handles the startup of the application.
    It initializes the cron job scheduler and registers the report jobs.
    """
    app.state.scheduler = (scheduler := get_scheduler())

    register_report_jobs(scheduler)
    scheduler.start()

    logger.info(f"Scheduled jobs: {len(scheduler.get_scheduled_jobs())}")
    for job in scheduler.get_scheduled_jobs():
        logger.info(f"Job ({job.id}): {job}")


async def shutdown(app: FastAPI):
    """
    Handles the shutdown of the application.
    It makes sure that the cron jobs are stopped.
    """
    logger.info("Shutting down Job scheduler...")
    app.state.scheduler.shutdown()

    logger.info("Shutdown complete")
