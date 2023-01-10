import json

from kafka import KafkaConsumer, KafkaProducer
import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from core.config import settings


class KafkaClient:
    """
    Kafka client for working with messages.
    """

    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.consumer = None
        self.producer = None

    async def start_consumer(self, topic, group_id=None, value_serializer=lambda x: x):
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

    async def start_producer(
            self, value_serializer=lambda v: json.dumps(v).encode("utf-8")
    ):
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

    async def produce_message(self, topic, message, key, timestamp_ms=None):
        if self.producer:
            await self.producer.send_and_wait(
                topic=topic, message=message, key=key, timestamp_ms=timestamp_ms
            )

        raise Exception("Producer is not started.")

    async def consume_messages(self, topic):
        if self.consumer:
            async for msg in self.consumer:
                yield msg

        raise Exception("Consumer is not started.")


kafka: KafkaClient = KafkaClient(
    bootstrap_servers=f"{settings.kafka.host}:{settings.kafka.port}"
)


def get_kafka() -> KafkaClient:
    """Function required for dependency injection"""
    return kafka
