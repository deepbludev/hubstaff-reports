from typing import List

from loguru import logger
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.core.config import Config


class EmailSender:
    """Email sender utility class using SendGrid."""

    def __init__(self, config: Config.EmailConfig):
        self.api_key = config.sendgrid_api_key
        self.from_address = config.from_address
        self.client = SendGridAPIClient(self.api_key)

    def send_html_email(
        self,
        subject: str,
        html_content: str,
        recipients: List[str],
    ) -> None:
        """Send an HTML email to the specified recipients using SendGrid."""
        message = Mail(
            from_email=self.from_address,
            to_emails=recipients,
            subject=subject,
            html_content=html_content,
        )

        try:
            self.client.send(message)
            logger.info(f"Email sent successfully to {recipients}")
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            raise
