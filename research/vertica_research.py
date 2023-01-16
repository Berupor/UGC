import datetime
import json

import vertica_python
import csv

connection_info = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': True,
}

with vertica_python.connect(**connection_info) as connection:  # 1
    cursor = connection.cursor()
    cursor.execute("""
        DROP TABLE IF EXISTS test;
        """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test (
        id VARCHAR(256) NOT NULL,
        viewpoint VARCHAR(256) NOT NULL,
        date VARCHAR(256) NOT NULL
    );
    """)
    start_time = datetime.datetime.now()
    with open("test.csv", "rb") as fs:
        cursor.copy("COPY test (id, viewpoint, date) FROM stdin DELIMITER ',' ", fs)
    total_time = datetime.datetime.now() - start_time
    print('done in: ', total_time)

    with open('results.json', 'r') as r:
        json_results = json.load(r)
        json_results["vertica_time"] = str(total_time)

    with open('results.json', 'w') as r:
        json.dump(json_results, r)

    #cursor.execute("""
    #    SELECT * FROM test;
    #""")
    #for row in cursor.iterate():
    #    print(row)
