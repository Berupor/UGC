import logging

from clickhouse_driver import Client

logging.basicConfig(level=logging.INFO)

client = Client(host='clickhouse-node1')
#client = Client(host='localhost')



def ch_kafka_queue(client: Client):
    client.execute(
        """
        CREATE TABLE entry_events_queue
            (
                timestamp DateTime,
                event String
            )
        ENGINE = Kafka
        SETTINGS
        kafka_broker_list = 'kafka:9192',
        kafka_topic_list = 'entry-events',
        kafka_group_name = 'group_events',
        kafka_format = 'JSONEachRow'
        """)


def ch_table(client: Client):
    client.execute(
        """
        CREATE TABLE entry_events
            (
                timestamp DateTime,
                event String
            )
        ENGINE = MergeTree
        ORDER BY timestamp
        """)


def ch_kafa_consumer(client: Client):
    client.execute(
        """
        CREATE MATERIALIZED VIEW materialized_view TO entry_events
        AS SELECT timestamp AS timestamp, event AS event
        FROM entry_events_queue
        ORDER BY timestamp
        """)


if __name__ == '__main__':
    ch_kafka_queue(client)
    logging.info('created clickhouse kafka queue table')
    ch_table(client)
    logging.info('created clickhouse table: entry_events')
    ch_kafa_consumer(client)
    logging.info('created clickhouse kafka consumer table')
