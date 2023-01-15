from pydantic import BaseSettings


class KafkaEngineSettings(BaseSettings):
    host: str = 'kafka_dev'
    port: str = '9192'
    topic: str = 'views'


kafka_engine_settings = KafkaEngineSettings()
