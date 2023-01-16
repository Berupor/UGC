# import datetime
# import csv
#
# import json
#
# from clickhouse_driver import Client
#
#
# client = Client(host="localhost")
#
#
# def ch_drop(client: Client):
#     client.execute("""DROP TABLE  IF EXISTS  test;""")
#
#
# def ch_table(client: Client):
#     client.execute(
#         """
#             CREATE TABLE  IF NOT EXISTS  test
#                     (
#                         id String,
#                         viewpoint String,
#                         date String
#                     )
#                 ENGINE = MergeTree
#                 ORDER BY id;
#         """
#     )
#
#
# def row_reader():
#     with open('test_data/test.csv') as test_csv:
#         for line in csv.reader(test_csv):
#             yield line
#
#
# with open('test_data/test.csv') as f:
#     ch_drop(client)
#     ch_table(client)
#     start_time = datetime.datetime.now()
#     client.execute('INSERT INTO test VALUES', (line for line in row_reader()))
#     total_time = datetime.datetime.now() - start_time
#     print('done in: ', total_time)
#
#     with open('results.json', 'r') as r:
#         json_results = json.load(r)
#         json_results["clickhouse_time"] = str(total_time)
#
#     with open('results.json', 'w') as r:
#         json.dump(json_results, r)
#
#
#
# print(client.execute('SELECT * FROM test'))