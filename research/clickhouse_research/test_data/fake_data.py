import csv


def data_generator():
    """
    Return generator for testing data consuming
    """
    with open("./test_data/test.csv") as test_csv:
        for line in csv.reader(test_csv):
            yield line
