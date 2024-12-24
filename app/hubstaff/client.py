from datetime import date
from typing import Annotated

import httpx
from fastapi import Depends
from loguru import logger

from app.core.config import get_config
from app.hubstaff.models import Credentials, DailyActivity, Organization, Pagination


class HubstaffClient:

    def __init__(self):
        settings = get_config()
        self.base_url = settings.hubstaff.api_url.rstrip("/")
        self.app_token = settings.hubstaff.app_token
        self.org_id = settings.hubstaff.organization_id
        self.email = settings.hubstaff.username
        self.password = settings.hubstaff.password
        self.auth_token: str | None = None

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(60.0, connect=30.0),
        )

    def header(self):
        """Header for the API requests, including the app token."""
        return {"AppToken": self.app_token}

    def token(self):
        """Auth token params for the API requests."""
        return {"auth_token": self.auth_token}

    def base_params(self, pagination: Pagination | None = None):
        """Params for the API requests."""
        pagination = pagination or Pagination()
        return self.token() | pagination.model_dump()

    async def login(self):
        """Login to Hubstaff."""

        endpoint = "people/auth"
        logger.info(f"Logging in to Hubstaff as {self.email}")

        response = await self.client.post(
            endpoint,
            headers=self.header(),
            data=Credentials(email=self.email, password=self.password).model_dump(),
        )
        response.raise_for_status()
        self.auth_token = response.json()["auth_token"]
        return self

    async def get_organizations(
        self, pagination: Pagination | None = None
    ) -> list[Organization]:
        """Get the available organizations."""
        endpoint = "companies"

        await self.login()
        response = await self.client.get(
            endpoint,
            headers=self.header(),
            params=self.base_params(pagination),
        )
        data = response.raise_for_status().json()["organizations"]
        return [Organization.model_validate(org) for org in data]

    async def get_work_by_day(
        self,
        start_date: date,
        stop_date: date,
        pagination: Pagination | None = None,
    ) -> list[DailyActivity]:
        """Get the work by day."""
        endpoint = f"companies/{self.org_id}/work/by_day"
        date_params = {
            "date[start]": start_date.isoformat(),
            "date[stop]": stop_date.isoformat(),
        }

        await self.login()
        response = await self.client.get(
            endpoint,
            headers=self.header(),
            params=self.base_params(pagination) | date_params,
        )
        logger.debug(response.json())
        data = response.raise_for_status().json()["daily_activities"]
        return [DailyActivity.model_validate(activity) for activity in data]


HubstaffClientDep = Annotated[HubstaffClient, Depends()]
