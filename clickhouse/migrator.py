from clickhouse_driver import Client

client = Client(host='clickhouse-node1')


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
        Engine=MergeTree() 
        ORDER BY timestamp
        """)

if __name__ == '__main__':
    ch_database(client)
    ch_table(client)