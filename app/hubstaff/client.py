from typing import Annotated

import httpx
from fastapi import Depends
from loguru import logger

from app.core.config import get_config
from app.hubstaff.models import Credentials, Organization


class HubstaffClient:

    def __init__(self):
        settings = get_config()
        self.base_url = settings.hubstaff.api_url.rstrip("/")
        self.app_token = settings.hubstaff.app_token
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

    async def login(self):
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

    async def get_organizations(self) -> list[Organization]:
        endpoint = "companies"
        await self.login()

        response = await self.client.get(
            endpoint,
            headers=self.header(),
            params=self.token(),
        )
        data = response.raise_for_status().json()["organizations"]
        return [Organization(**org) for org in data]


HubstaffClientDep = Annotated[HubstaffClient, Depends()]
