from configure.mongo_client import mongo_client
import sys
# from test_data.fake_data import rating_data_generator
from test_data.generate_fake_data import generate_ratings
import time

sys.path.append("..")
from research.speed_test import MongoSpeedTest

# Prepare mongo
db = mongo_client.movies
ratings_collection = db.ratings
mongo_speed_test = MongoSpeedTest(mongo_client)


def insert():
    start_time = time.time()

    for rating in generate_ratings():
        mongo_speed_test.test_insert_data(ratings_collection, rating)

    end_time = time.time()
    exec_time = end_time - start_time
    print('Запись данных произошла за', round(exec_time, 1), 'секунд')


insert()
