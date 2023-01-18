from faker import Faker
import csv


def generate_ratings():
    faker = Faker()
    for _ in range(100):
        yield {
            "movie_name": faker.sentence(nb_words=3),
            "likes": faker.random_int(min=0, max=10000, step=1),
            "dislikes": faker.random_int(min=0, max=1000, step=1)
        }
