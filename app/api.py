from datetime import date

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app import reports
from app.hubstaff.client import HubstaffClientDep

# region: api
reports_api_router = APIRouter(prefix="/v1/reports")


@reports_api_router.get("/activity")
async def daily_activity_report(
    hubstaff_client: HubstaffClientDep,
    report_date: date | None = None,
):
    """Get the daily activity summary report."""
    return await reports.daily_activity(
        hubstaff_client, report_date=report_date or date.today()
    )


# endregion: api

# region: html
reports_html_router = APIRouter(prefix="/reports")


@reports_html_router.get("/activity", response_class=HTMLResponse)
async def daily_activity_report_html(
    hubstaff_client: HubstaffClientDep,
    report_date: date | None = None,
):
    """Get the daily activity summary report as HTML."""
    report = await reports.daily_activity(
        hubstaff_client, report_date=report_date or date.today()
    )
    return report.to_html()


# endregion: html
