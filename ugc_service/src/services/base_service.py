from json import loads

from fastapi import Depends

from event_streamer.kafka_streamer import KafkaClient, get_kafka
from typing import Dict, Union, Any, AsyncGenerator
from pydantic import BaseModel


class EventService:
    def __init__(self, kafka: KafkaClient):
        self.kafka_client = kafka

    async def produce(self, key: str, topic_name: str, data: Union[Dict, BaseModel]) -> None:
        if type(data) != dict:
            data = data.json()  # type: ignore

        await self.kafka_client.produce_message(
            key=str.encode(key), topic=topic_name, value=loads(data)
        )

    async def consume(self, topic: str, group_id=None) -> AsyncGenerator:
        """
        Example usage:

        async for message in await service.consume('views'):
            print(message)
        """
        return self.kafka_client.consume_messages(topic, group_id)


def get_event_service(kafka: KafkaClient = Depends(get_kafka)) -> EventService:
    return EventService(kafka)
