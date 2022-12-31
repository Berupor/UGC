"""Settings"""

import os

from pydantic import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_DIR = os.path.join(BASE_DIR, "..", "..")


class ClickHouseSettings(BaseSettings):
    host: str
    username: str
    password: str
    port: int


class Settings(BaseSettings):
    clickhouse: ClickHouseSettings

    class Config:
        #  For local development outside of docker
        env_file = (
            os.path.join(ENV_DIR, ".env.prod"),
            os.path.join(ENV_DIR, ".env.dev"),
        )
        env_nested_delimiter = "__"


settings = Settings()
