from db.clickhouse.clickhouse_client import ch_client
from db.clickhouse.data_scheme import init_ch
from speed_test import DBSpeedTest, VerticaSpeedTest
from test_data.fake_data import data_generator, post_data
from db.vertica.vertica_client import vt_client

from db.vertica.data_scheme import init_vertica

ch_speed_test = DBSpeedTest(ch_client)
init_ch(ch_client)

vertica_speed_test = VerticaSpeedTest(vt_client.cursor())
init_vertica(vt_client.cursor())


def test_insert():
    a = ch_speed_test.test_insert_data('INSERT INTO test VALUES', (line for line in data_generator()))
    b = vertica_speed_test.test_insert_data(data='test.csv',
                                            query="COPY test (id, viewpoint, date) FROM stdin DELIMITER ',' ")
    diff = b / a * 100 - 100
    print(f"Clickhouse быстрее на {diff}%")


test_insert()
