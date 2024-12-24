from datetime import date, timedelta

from loguru import logger

from app.core.config import get_config
from app.core.scheduler import Scheduler
from app.hubstaff.client import HubstaffClient
from app.reports import daily_activity


async def generate_daily_report():
    """Generate the daily activity report for the previous day."""
    yesterday = date.today() - timedelta(days=1)
    logger.info(f"Generating daily activity report for {yesterday}")

    client = HubstaffClient()
    report = await daily_activity(client, report_date=yesterday)

    logger.info(f"Daily activity report generated for {yesterday}: {report}")
    # TODO: Save report to output directory as HTML file


def register_report_jobs(scheduler: Scheduler) -> None:
    """Register the daily report job with the scheduler."""
    config = get_config()
    scheduler.register(
        name="Generate daily activity report by user and project.",
        job_id="daily_activity_report",
        job=generate_daily_report,
        cron=config.reports.report_time,
    )
