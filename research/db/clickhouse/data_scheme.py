from clickhouse_driver import Client



def create_ch_table(client: Client):
    client.execute(
        """
            CREATE TABLE  IF NOT EXISTS  test
                    (
                        id String,
                        viewpoint String,
                        date String
                    )
                ENGINE = MergeTree
                ORDER BY id;
        """
    )

def flush_db(client: Client):
    client.execute("""DROP TABLE  IF EXISTS  test;""")
