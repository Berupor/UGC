import random
import uuid
from faker import Faker
import csv

import json

fake = Faker()

def fake_data():
    event_id = uuid.uuid4()
    viewpoint = random.randint(10000, 99999)
    timestamp = fake.date_time_this_year()
    return [event_id, viewpoint, timestamp]


with open('test_data/test.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'viewpoint', 'timestamp'])
    for i in range(1, 1000):
        writer.writerow(fake_data())
    results = {"clickhouse_time": "not tested",
               "vertica_time": "not tested"}

    with open('results.json', 'w') as r:
        json.dump(results, r)