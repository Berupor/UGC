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


def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__doc__}: выполнилось за {round(end - start, 4)} секунд")
        return result

    return wrapper


@measure_time
def insert(collection, generator):
    """Запись данных"""
    for rating in generator(3000):
        mongo_speed_test.test_insert_data(collection, rating)


@measure_time
def read():
    """Чтение данных"""
    mongo_speed_test.test_get_data(ratings_collection, {"likes": {"$gt": 1000}})


def real_time_read():
    ratings_collection.insert_one({"name": "movie5", "likes": 1000, "dislikes": 500})

    start_time = time.time()

    movie_data = mongo_speed_test.test_get_data(ratings_collection, {"name": "movie5"})
    while not movie_data:
        movie_data = mongo_speed_test.test_get_data(
            ratings_collection, {"name": "movie5"}
        )

    end_time = time.time()
    print(
        "Real-time чтение данных выполнилось за:",
        round(end_time - start_time, 4),
        "секунд",
    )


def main():
    insert(ratings_collection, generate_ratings)
    insert(users_collection, generate_user_likes)
    read()
    real_time_read()

    mongo_client.close()


if __name__ == "__main__":
    main()
