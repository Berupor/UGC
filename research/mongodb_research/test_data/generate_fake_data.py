import csv

from faker import Faker


def generate_ratings():
    faker = Faker()
    for _ in range(3000):
        yield {
            "movie_name": faker.sentence(nb_words=3),
            "likes": faker.random_int(min=0, max=2000, step=1),
            "dislikes": faker.random_int(min=0, max=2000, step=1),
        }


def generate_user_likes():
    faker = Faker()
    for _ in range(3000):
        yield {
            "name": faker.sentence(nb_words=1),
            "likes": [
                faker.sentence(nb_words=3),
                faker.sentence(nb_words=3),
                faker.sentence(nb_words=3),
            ],
        }
