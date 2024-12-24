from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.hubstaff.client import HubstaffClientDep


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


@app.get("/reports/activity")
async def get_activity_report(hubstaff_client: HubstaffClientDep):
    """Get the activity report."""
    return await hubstaff_client.get_organizations()


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
