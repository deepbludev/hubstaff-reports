from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class HubstaffConfig(BaseModel):
    api_url: str
    app_token: str
    organization_id: str
    username: str
    password: str


class ReportConfig(BaseModel):
    output_dir: str
    report_time: str


class Settings(BaseSettings):
    hubstaff: HubstaffConfig
    reports: ReportConfig

    @classmethod
    def from_yaml(cls, path: str | Path):
        with open(path) as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data)


@lru_cache()
def get_settings() -> Settings:
    return Settings.from_yaml("config.yaml")
