from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    @classmethod
    def from_yaml(cls, path: str | Path):
        """Load settings from a YAML config file."""
        with open(path) as f:
            config_data = yaml.safe_load(f)
        return cls.model_validate(config_data)

    hubstaff: HubstaffConfig
    reports: ReportConfig
    email: EmailConfig

    class HubstaffConfig(BaseModel):
        """Hubstaff configuration."""

        api_url: str
        app_token: str
        organization_id: int
        username: str
        password: str

    class ReportConfig(BaseModel):
        """Report configuration."""

        output_dir: str
        report_time: str
        recipients: list[str]

    class EmailConfig(BaseModel):
        """Email configuration."""

        sendgrid_api_key: str
        from_address: str


@lru_cache()
def get_config() -> Config:
    return Config.from_yaml("config.yaml")
