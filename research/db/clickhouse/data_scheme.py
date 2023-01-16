from clickhouse_driver import Client



def init_ch(client: Client):
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

def flush_ch(client: Client):
    client.execute("""DROP TABLE  IF EXISTS  test;""")
