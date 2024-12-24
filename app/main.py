from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.core.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles the lifespan of the FastAPI app.
    """
    await startup(app)
    yield
    await shutdown(app)


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "OK"}


async def startup(app: FastAPI):
    """
    Handles the startup of the application.
    It initializes the cron job scheduler.
    """
    settings = get_settings()
    logger.info(settings)


async def shutdown(app: FastAPI):
    """
    Handles the shutdown of the application.
    It makes sure that the cron jobs are stopped.
    """
    pass
