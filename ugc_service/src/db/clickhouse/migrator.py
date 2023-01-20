import logging
from time import sleep

from clickhouse_driver import Client  # type: ignore

logging.basicConfig(level=logging.INFO)

client = Client(host="clickhouse-node1")


def ch_kafka_queue(client: Client):
    client.execute(
        f"""
            CREATE TABLE IF NOT EXISTS entry_events_queue
                (
                    id String,
                    viewpoint UInt64,
                    datetime_event Datetime
                )
            ENGINE = Kafka
            SETTINGS
            kafka_broker_list = 'broker:9192',
            kafka_topic_list = 'views',
            kafka_group_name = 'group_events',
            kafka_format = 'JSONEachRow',
            kafka_row_delimiter = '\n';
        """
    )


def ch_table(client: Client):
    client.execute(
        """
            CREATE TABLE  IF NOT EXISTS  entry_events
                    (
                        id String,
                        viewpoint UInt64,
                        datetime_event Datetime
                    )
                ENGINE = MergeTree PARTITION BY toYYYYMMDD(datetime_event)
                ORDER BY id;
        """
    )


def ch_kafa_consumer(client: Client):
    client.execute(
        """
        CREATE MATERIALIZED VIEW IF NOT EXISTS materialized_view TO entry_events
        AS SELECT *
        FROM entry_events_queue
        ORDER BY id;
        """
    )


def init_ch():
    sleep(10)
    ch_kafka_queue(client)
    logging.info("created clickhouse kafka_dev queue table")
    ch_table(client)
    logging.info("created clickhouse table: entry_events")
    ch_kafa_consumer(client)
    logging.info("created clickhouse kafka_dev consumer table")
