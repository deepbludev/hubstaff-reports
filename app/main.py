from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api import reports_router


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
    It initializes the cron job scheduler.
    """
    pass


async def shutdown(app: FastAPI):
    """
    Handles the shutdown of the application.
    It makes sure that the cron jobs are stopped.
    """
    pass
