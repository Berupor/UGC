import logging

from clickhouse_driver import Client

from migrator_settings import kafka_engine_settings

logging.basicConfig(level=logging.INFO)

client = Client(host='clickhouse-node1')


def ch_kafka_queue(client: Client):
    client.execute(
        f"""
        CREATE TABLE IF NOT EXISTS entry_events_queue
            (
                message String
            )
        ENGINE = Kafka
        SETTINGS
        kafka_broker_list = '{kafka_engine_settings.host}:{kafka_engine_settings.port}',
        kafka_topic_list = '{kafka_engine_settings.topic}',
        kafka_group_name = 'group_events',
        kafka_format = 'JSONAsString',
        kafka_row_delimiter = '\n'
        """)


def ch_table(client: Client):
    client.execute(
        """
        CREATE TABLE IF NOT EXISTS entry_events
            (
                timestamp_ms DateTime,
                id String,
                value String
            )
        ENGINE = MergeTree
        ORDER BY timestamp_ms
        """)


def ch_kafa_consumer(client: Client):
    client.execute(
        """
        CREATE MATERIALIZED VIEW IF NOT EXISTS materialized_view TO entry_events
        AS SELECT 
            toDateTime(JSONExtractUInt(message, 'timestamp_ms')) AS timestamp_ms,
            JSONExtractString(message, 'id') AS id,
            JSONExtractString(message, 'value') AS value
        FROM entry_events_queue
        """)


if __name__ == '__main__':
    ch_kafka_queue(client)
    logging.info('created clickhouse kafka_dev queue table')
    ch_table(client)
    logging.info('created clickhouse table: entry_events')
    ch_kafa_consumer(client)
    logging.info('created clickhouse kafka_dev consumer table')
