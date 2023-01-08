from fastapi import Depends

from kafka_client.event_streamer import KafkaClient, get_kafka


class EventService:

    def __init__(self, kafka: KafkaClient):
        self.kafka_client = kafka

    def produce(self, key, topic_name, model) -> None:
        self.kafka_client.produce_message(
            key=str.encode(key),
            topic=topic_name,
            message=model.value.json(),
            timestamp_ms=model.timestamp_ms,
        )


def get_event_service(kafka: KafkaClient = Depends(get_kafka)) -> EventService:
    return EventService(kafka)
