import sys

from db.clickhouse.clickhouse_client import ch_client
from db.clickhouse.data_scheme import flush_ch, init_ch
from db.vertica.data_scheme import flush_vertica, init_vertica
from db.vertica.vertica_client import vt_client
from test_data.fake_data import data_generator

sys.path.append("..")
from research.speed_test import CHSpeedTest, VerticaSpeedTest

ch_speed_test = CHSpeedTest(ch_client)
flush_ch(ch_client)
init_ch(ch_client)

vertica_speed_test = VerticaSpeedTest(vt_client.cursor())
flush_vertica(vt_client.cursor())
init_vertica(vt_client.cursor())


def test_insert():
    ch_speed_test.test_insert_data(
        "INSERT INTO test VALUES", (line for line in data_generator())
    )
    a = ch_speed_test.test_insert_data_exec_time
    vertica_speed_test.test_insert_data(
        data="test.csv",
        query="COPY test (id, viewpoint, date) FROM stdin DELIMITER ',' ",
    )
    b = vertica_speed_test.test_insert_data_exec_time

    diff = b / a * 100 - 100
    print(f"Clickhouse быстрее записал данные на {round(diff, 1)}%")


def test_read():
    ch_speed_test.test_get_data("select * from test")
    a = ch_speed_test.test_get_data_exec_time
    vertica_speed_test.test_get_data("select * from test")
    b = vertica_speed_test.test_get_data_exec_time
    diff = b / a * 100 - 100
    print(f"Clickhouse быстрее считал данные на {round(diff, 1)}%")


test_read()
test_insert()
