import random
import uuid
import datetime

from faker import Faker
import json
import logging
import time
from clickhouse_driver import Client
import vertica_python

fake = Faker()
client = Client(host="localhost")


def ch_drop(client: Client):
    client.execute(
        """
            DROP TABLE  IF EXISTS  test;
        """
    )


def ch_table(client: Client):
    client.execute(
        """
            CREATE TABLE  IF NOT EXISTS  test
                    (
                        id String,
                        viewpoint UInt64,
                        datetime_event Date
                    )
                ENGINE = MergeTree PARTITION BY toYYYYMMDD(datetime_event)
                ORDER BY id;
        """
    )


def ch_load(client: Client):
    for i in range(1000):
        data = {
            "id": str(uuid.uuid4()),
            "viewpoint": random.randint(1000, 9999),
            "datetime_event": str(fake.date())
        }
        m = json.dumps(data)
        client.execute(f'''INSERT INTO test FORMAT JSONEachRow {m}''')




if __name__ == '__main__':
    ch_drop(client)
    ch_table(client)
    start_time = datetime.datetime.now()
    ch_load(client)
    total_time = datetime.datetime.now() - start_time
    print('done in: ', total_time)
