from datetime import date, timedelta
from pathlib import Path

from loguru import logger

from app.core.config import get_config
from app.core.email import EmailSender
from app.core.scheduler import Scheduler
from app.hubstaff.client import HubstaffClient
from app.reports import daily_activity


async def generate_daily_report():
    """Generate the daily activity report for the previous day."""
    yesterday = date.today() - timedelta(days=1)
    logger.info(f"Generating daily activity report for {yesterday}")

    # generate the report in HTML format
    client = HubstaffClient()
    report = await daily_activity(client, report_date=yesterday)
    report_html = report.to_html()

    # save the report to a file
    config = get_config()
    output_dir = Path.cwd() / config.reports.output_dir.lstrip("/")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"daily_activity_{yesterday.isoformat()}.html"
    output_file.write_text(report_html)
    logger.info(f"Daily activity report saved to {output_file}")

    # send email notifications
    if config.reports.recipients:
        sender = EmailSender(config.email)
        try:
            sender.send_html_email(
                subject=f"Hubstaff Daily Activity Report - {report.date.isoformat()}",
                html_content=report_html,
                recipients=config.reports.recipients,
            )
            logger.info("Daily activity report email sent successfully")
        except Exception as e:
            logger.error(f"Failed to send daily activity report email: {str(e)}")


def register_report_jobs(scheduler: Scheduler) -> None:
    """Register the daily report job with the scheduler."""
    config = get_config()
    scheduler.register(
        name="Generate daily activity report by user and project.",
        job_id="daily_activity_report",
        job=generate_daily_report,
        cron=config.reports.report_time,
    )
