import os
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Config(BaseSettings):
    """Основные настройки проекта - подключения к другим сервисам и прочее."""

    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = Field(env="PROJECT_NAME", default="movies")

    # Корень проекта
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    secret_key: str = Field(env="secret_key", default="super-secret")
    token_algo: str = Field(env="token_algo", default="HS256")

    class Config:
        env_file = ".env"
