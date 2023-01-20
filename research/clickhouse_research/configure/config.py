"""Settings"""

from pydantic import BaseSettings


class ClickHouseSettings(BaseSettings):
    host: str
    port: int


class Settings(BaseSettings):
    clickhouse: ClickHouseSettings

    class Config:
        env_file = "../.env.prod"
        env_nested_delimiter = "__"


settings = Settings()
