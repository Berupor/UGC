from db.clickhouse.clickhouse_client import ch_client
from db.clickhouse.data_scheme import create_ch_table
from speed_test import DBSpeedTest
from test_data.fake_data import data_generator

ch_speed_test = DBSpeedTest(ch_client)
create_ch_table(ch_client)

print(ch_speed_test.test_insert_data('INSERT INTO test VALUES', (line for line in data_generator())))
