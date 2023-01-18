import csv


def rating_data_generator():
    """
    Return generator for testing data consuming
    """
    with open("test_data/fake_data.csv") as test_csv:
        for line in csv.reader(test_csv):
            print((line))
            yield line
