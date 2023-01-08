from fastapi import Depends

from kafka_client.event_streamer import KafkaClient, get_kafka
from services.base import BaseService

from models.film import FilmWatchEvent


class FilmWatchService(BaseService):
    _model = FilmWatchEvent
    _topic_name = "views"


def get_film_watch_service(kafka: KafkaClient = Depends(get_kafka)) -> FilmWatchService:
    return FilmWatchService(kafka)
