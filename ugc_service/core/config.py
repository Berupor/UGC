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

    class Config:
        env_file = ".env"
