from datetime import date

from fastapi import APIRouter

from app import reports
from app.hubstaff.client import HubstaffClientDep

reports_router = APIRouter(prefix="/reports")


@reports_router.get("/activity")
async def daily_activity_report(
    hubstaff_client: HubstaffClientDep,
    report_date: date | None = None,
):
    """Get the daily activity summary report."""
    return await reports.daily_activity(
        hubstaff_client, report_date=report_date or date.today()
    )
