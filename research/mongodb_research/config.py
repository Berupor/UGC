"""Settings"""

from pydantic import BaseSettings


class MongoSettings(BaseSettings):
    host: str
    port: int
    username: str
    password: str


class Settings(BaseSettings):
    mongo: MongoSettings

    class Config:
        env_file = ".env.prod"
        env_nested_delimiter = "__"


settings = Settings()
