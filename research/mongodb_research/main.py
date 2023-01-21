import time

from configure.mongo_client import mongo_client
from test_data.generate_fake_data import generate_ratings, generate_user_likes

from research.speed_test import MongoSpeedTest

# Prepare mongo
db = mongo_client.movies

ratings_collection = db.ratings
ratings_collection.delete_many({})

users_collection = db.users
users_collection.delete_many({})

mongo_speed_test = MongoSpeedTest(mongo_client)


def insert(collection, generator):
    start_time = time.time()

    for rating in generator():
        mongo_speed_test.test_insert_data(collection, rating)

    end_time = time.time()
    print("Запись данных произошла за", round(end_time - start_time, 3), "секунд")


def read():
    start_time = time.time()

    query = {"likes": {"$gt": 1000}}
    mongo_speed_test.test_get_data(ratings_collection, query)

    end_time = time.time()
    print("Чтение данных произошло за", round(end_time - start_time, 5), "секунд")


def real_time_read():
    data = {"name": "movie5", "likes": 1000, "dislikes": 500}
    ratings_collection.insert_one(data)

    start_time = time.time()
    ratings_collection.find({"name": "movie"})
    end_time = time.time()

    print(
        "Real-time чтение данных произошло за: ",
        round(end_time - start_time, 5),
        "секунд",
    )


insert(ratings_collection, generate_ratings)
insert(users_collection, generate_user_likes)
read()
real_time_read()

mongo_client.close()
