from kafka import KafkaProducer
from faker import Faker
import json
from json import dumps
import logging
import time


fake = Faker()

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='../producer.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x:
                         dumps(x).encode('utf-8'))


def kafka_load(producer: KafkaProducer):
    for i in range(10):
        data = {
            'timestamp': fake.date(),
            'event': str(fake.random_int(min=20000, max=100000))
        }
        producer.send(topic='entry-events', value=data)
        print(data)
        time.sleep(1)


if __name__ == '__main__':
    log_level = logging.DEBUG
    logging.basicConfig(level=log_level)
    log = logging.getLogger('kafka')
    log.setLevel(log_level)
    kafka_load(producer)
