from __future__ import annotations

from datetime import date

from app.hubstaff.client import HubstaffClient

from .daily_activity import DailyActivityReport


async def daily_activity(
    hubstaff_client: HubstaffClient,
    report_date: date,
) -> DailyActivityReport:
    daily_activities = await hubstaff_client.get_work_by_day(
        start_date=report_date,
        stop_date=report_date,
    )
    return DailyActivityReport.from_daily_activities(report_date, daily_activities)
