import random
import uuid
import datetime
import csv

from datetime import datetime
from faker import Faker
import json
import logging
import time
from clickhouse_driver import Client
import vertica_python

fake = Faker()
client = Client(host="localhost")


def ch_drop(client: Client):
    client.execute("""DROP TABLE  IF EXISTS  test;""")


def ch_table(client: Client):
    client.execute(
        """
            CREATE TABLE  IF NOT EXISTS  test
                    (
                        id Int64,
                        viewpoint Int64,
                        date Date
                    )
                ENGINE = MergeTree PARTITION BY toYYYYMMDD(date)
                ORDER BY id;
        """
    )


schema = {
    'id': int,
    'viewpoint ': int,
    'date': lambda x: datetime.strptime(x, '%Y-%m-%d').date(),
}
bypass = lambda x: x


with open('test.csv') as f:
    gen = ({k: schema.get(k, bypass)(v) for k, v in row.items()} for row in csv.DictReader(f))
    ch_drop(client)
    ch_table(client)
    client.execute('INSERT INTO test VALUES', gen)

print(client.execute('SELECT * FROM test'))