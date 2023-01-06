from kafka import KafkaConsumer, KafkaProducer
import json


class KafkaClient:
    def __init__(self, broker_url, topic):
        self.broker_url = broker_url
        self.topic = topic

    def produce_message(self, message):
        producer = KafkaProducer(
            bootstrap_servers=self.broker_url,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        producer.send(self.topic, message)

    def consume_messages(self):
        consumer = KafkaConsumer(self.topic, bootstrap_servers=self.broker_url)
        for message in consumer:
            yield message


# Using example
# client = KafkaClient("localhost:9092", "topic_name")
# client.produce_message(b"Your message")
# Or json format
# client.produce_message('fizzbuzz', {'foo': 'bar'})
#
# for message in client.consume_messages():
#     print(message.value)
