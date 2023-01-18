import time
from abc import ABC, abstractmethod


def time_it(method):
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        result = method(self, *args, **kwargs)
        end_time = time.time()
        exec_time = end_time - start_time

        setattr(self, method.__name__ + '_exec_time', exec_time)
        return result

    return wrapper


class SpeedTest(ABC):
    @abstractmethod
    def test_insert_data(self, query, data):
        ...

    @abstractmethod
    def test_get_data(self, query):
        ...


class CHSpeedTest(SpeedTest):
    def __init__(self, db_connection):
        self.db = db_connection

    @time_it
    def test_insert_data(self, query, data):
        self.db.execute(query, data)

    @time_it
    def test_get_data(self, query):
        self.db.execute(query)


class VerticaSpeedTest(SpeedTest):
    def __init__(self, cursor):
        self.cursor = cursor

    @time_it
    def test_insert_data(self, query, data):
        with open("clickhouse_research/test_data/test.csv", "rb") as fs:
            self.cursor.copy(
                "COPY test (id, viewpoint, date) FROM stdin DELIMITER ',' ", fs
            )

    @time_it
    def test_get_data(self, query):
        self.cursor.execute(query)
