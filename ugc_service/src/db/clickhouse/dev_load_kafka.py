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


producer = KafkaProducer(bootstrap_servers=['localhost:9092'])


def kafka_load(producer: KafkaProducer):
    for i in range(1000):
        data = {
            "timestamp": fake.date(),
            "event": "saturday"
        }
        m = json.dumps(data)
        producer.send(topic='views', value=m.encode('utf-8'))
        print(data)
        time.sleep(1)


if __name__ == '__main__':
    kafka_load(producer)
