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


class FastapiSettings(BaseSettings):
    project_name: str
    secret_key: str
    host: str
    port: int


class KafkaSettings(BaseSettings):
    host: str
    port: int
    topic: str


class ConnectSettings(BaseSettings):
    host: str
    port: int


class MongoSettings(BaseSettings):
    host: str
    port: int
    username: str
    password: str

class Logstash(BaseSettings):
    host: str
    port: int


class Settings(BaseSettings):
    token_algo: str

    fastapi: FastapiSettings
    mongo: MongoSettings
    kafka: KafkaSettings
    connect: ConnectSettings
    clickhouse: ClickHouseSettings
    logstash: Logstash

    class Config:
        #  For local development outside of docker
        env_file = (
            os.path.join(ENV_DIR, ".env.prod"),
            os.path.join(ENV_DIR, ".env.dev"),
        )
        env_nested_delimiter = "__"


settings = Settings()
