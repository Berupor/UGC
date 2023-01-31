import asyncio
import json
from typing import AsyncGenerator

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer  # type: ignore
from core.config import settings


class KafkaClient:
    """
    Kafka client for working with messages.
    """

    DEFAULT_CONS_SERIALIZER = lambda x: x
    JSON_PRODUCER_SERIALIZER = lambda v: json.dumps(v).encode("utf-8")
    DEFAULT_PRODUCER_SERIALIZER = lambda v: json.dumps(v).encode("utf-8")

    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.consumer = None
        self.producer = None

    async def _start_consumer(
        self, topic, group_id, value_serializer=DEFAULT_CONS_SERIALIZER
    ):
        if self.consumer:
            raise Exception("Consumer already started.")

        self.consumer = AIOKafkaConsumer(
            topic,
            loop=asyncio.get_event_loop(),
            bootstrap_servers=self.bootstrap_servers,
            group_id=group_id,
            value_deserializer=value_serializer,
        )

        await self.consumer.start()

    async def stop_consumer(self):
        if self.consumer is None:
            raise Exception("Consumer is not started.")

        await self.consumer.stop()
        self.consumer = None

    async def _start_producer(self, value_serializer=JSON_PRODUCER_SERIALIZER):
        if self.producer:
            raise Exception("Producer already started.")

        self.producer = AIOKafkaProducer(
            loop=asyncio.get_event_loop(),
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=value_serializer,
        )
        await self.producer.start()

    async def stop_producer(self):
        if self.producer is None:
            raise Exception("Producer is not started.")

        await self.producer.stop()
        self.producer = None

    async def produce_message(
        self,
        topic,
        value=None,
        key=None,
        partition=None,
        timestamp_ms=None,
        headers=None,
    ):
        if not self.producer:
            await self._start_producer()

        await self.producer.send_and_wait(
            topic, value, key, partition, timestamp_ms, headers
        )

    async def consume_messages(self, topic, group_id=None,) -> AsyncGenerator:
        if not self.consumer:
            await self._start_consumer(topic, group_id)

        async for msg in self.consumer:
            yield msg


kafka_client: KafkaClient = KafkaClient(
    bootstrap_servers=f"{settings.kafka.host}:{settings.kafka.port}"
)


def get_kafka() -> KafkaClient:
    """Function required for dependency injection"""
    return kafka_client
