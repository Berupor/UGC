from pydantic import BaseSettings


class KafkaEngineSettings(BaseSettings):
    host: str = 'kafka'
    port: str = '9092'
    topic: str = 'views'


kafka_engine_settings = KafkaEngineSettings()
