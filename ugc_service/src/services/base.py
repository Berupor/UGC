import os
import sys

from kafka_client.event_streamer import KafkaClient, get_kafka


class BaseService:
    def __init__(self, kafka: KafkaClient):
        self.kafka_client = kafka

    def produce(self, key, **attrs):
        model = self._model(**attrs)
        self.kafka_client.produce_message(
            key=key,
            topic=self._topic_name,
            value=model.value,
            timestamp_ms=model.timestamp_ms,
        )

        return model.json()
