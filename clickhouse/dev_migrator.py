import logging

from clickhouse_driver import Client

logging.basicConfig(level=logging.INFO)

client = Client(host='clickhouse-node1')


def ch_kafka_queue(client: Client):
    client.execute(
        """
        CREATE TABLE IF NOT EXISTS ugc.views_queue 
            (
                user_id String,
                filmwork_id String,
                viewed_frame UInt64,
                timestamp DateTime('Europe/Moscow') 
            ) 
        ENGINE=Kafka('localhost:9092', 'views', 'views_group', 'JSONEachRow');
        """)


def ch_database(client: Client):
    client.execute("CREATE DATABASE IF NOT EXISTS ugc ON CLUSTER company_cluster")
    return True


def ch_table(client: Client):
    client.execute(
        """
        CREATE TABLE ugc.views ON CLUSTER company_cluster 
            (
                user_id String,
                filmwork_id String,
                viewed_frame UInt64,
                timestamp DateTime('Europe/Moscow') 
            ) 
        Engine=ReplacingMergeTree() 
        ORDER BY timestamp
        """)


def ch_kafa_consumer(client: Client):
    client.execute(
        """
        CREATE MATERIALIZED VIEW ugc.views_consumer
        TO ugc.views
        AS SELECT *
        FROM ugc.views_queue;
        """)


if __name__ == '__main__':
    ch_database(client)
    logging.info('created clickhouse database: ugc')
    ch_kafka_queue(client)
    logging.info('created clickhouse kafka queue table')
    ch_table(client)
    logging.info('created clickhouse table: views')
    ch_kafa_consumer(client)
    logging.info('created clickhouse kafka consumer table')
