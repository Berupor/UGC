import time
from abc import ABC, abstractmethod


class SpeedTest(ABC):

    @abstractmethod
    def test_insert_data(self, query, data):
        ...

    @abstractmethod
    def test_get_data(self, query):
        ...


class ClickhouseSpeedTest(SpeedTest):

    def __init__(self, db_connection):
        self.db = db_connection

    def test_insert_data(self, query, data):
        start_time = time.time()
        self.db.execute(query)
        end_time = time.time()
        return end_time - start_time

    def test_get_data(self, query):
        start_time = time.time()
        self.db.execute(query)
        end_time = time.time()
        return end_time - start_time
