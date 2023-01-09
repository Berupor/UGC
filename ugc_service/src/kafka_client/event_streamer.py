import json

from kafka import KafkaConsumer, KafkaProducer

from core.config import settings


class KafkaClient:
    """
    Kafka client for working with messages.

    Using example:
    client = KafkaClient("localhost:9092", "topic_name")
    client.produce_message(b"Your message")
    Or json format
    client.produce_message('fizzbuzz', {'foo': 'bar'})

    for message in client.consume_messages():
        print(message.value)
    """

    def __init__(self, broker_url):
        self.broker_url = broker_url

    def produce_message(self, message, topic, key, timestamp_ms=None):
        producer = KafkaProducer(
            bootstrap_servers=self.broker_url,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        producer.send(topic, message, key)

    def consume_messages(self, topic):
        consumer = KafkaConsumer(topic, bootstrap_servers=self.broker_url)
        for message in consumer:
            yield message


kafka: KafkaClient = KafkaClient(
    broker_url=f"{settings.kafka.host}:{settings.kafka.port}"
)


def get_kafka() -> KafkaClient:
    """Function required for dependency injection"""
    return kafka
