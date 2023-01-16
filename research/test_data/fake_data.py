import csv


def data_generator():
    """
    Return generator for testing data consuming
    """
    with open('test_data/test.csv') as test_csv:
        for line in csv.reader(test_csv):
            yield line

def post_data():
    """
    Return csv data for file writing to db
    """
    with open('test_data/test.csv', 'rb') as file:
        data = file.read()
        return data
