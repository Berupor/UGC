from fastapi import Depends
from json import loads

from event_streamer.kafka_streamer import KafkaClient, get_kafka


class EventService:
    def __init__(self, kafka: KafkaClient):
        self.kafka_client = kafka

    async def produce(self, key, topic_name, model) -> None:
        data = loads(model.json())
        data["id"] = key
        await self.kafka_client.produce_message(
            key=str.encode(key),
            topic=topic_name,
            value=data
        )

    async def consume(self, topic, group_id=None):
        """
        Example usage:

        async for message in await service.consume('views'):
            print(message)
        """
        return self.kafka_client.consume_messages(topic, group_id)


def get_event_service(kafka: KafkaClient = Depends(get_kafka)) -> EventService:
    return EventService(kafka)
