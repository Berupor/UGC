import logging

from clickhouse_driver import Client

from migrator_settings import kafka_engine_settings

logging.basicConfig(level=logging.INFO)

client = Client(host='clickhouse-node1')


def ch_kafka_queue(client: Client):
    client.execute(
        f"""
        CREATE TABLE entry_events_queue
            (
                id UUID,
                value String,
                name String,
                timestamp DateTime
            )
        ENGINE = Kafka
        SETTINGS
        kafka_broker_list = '{kafka_engine_settings.host}:{kafka_engine_settings.port}',
        kafka_topic_list = '{kafka_engine_settings.topic}',
        kafka_group_name = 'group_events',
        kafka_format = 'JSONEachRow'
        """)


def ch_table(client: Client):
    client.execute(
        """
        CREATE TABLE entry_events
            (
                id UUID,
                value String,
                name String,
                timestamp DateTime
            )
        ENGINE = MergeTree
        ORDER BY timestamp
        """)


def ch_kafa_consumer(client: Client):
    client.execute(
        """
        CREATE MATERIALIZED VIEW materialized_view TO entry_events
        AS SELECT *
        FROM entry_events_queue
        ORDER BY timestamp
        """)


if __name__ == '__main__':
    ch_kafka_queue(client)
    logging.info('created clickhouse kafka_dev queue table')
    ch_table(client)
    logging.info('created clickhouse table: entry_events')
    ch_kafa_consumer(client)
    logging.info('created clickhouse kafka_dev consumer table')
