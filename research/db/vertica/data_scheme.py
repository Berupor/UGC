def init_vertica(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS test (
            id VARCHAR(256) NOT NULL,
            viewpoint VARCHAR(256) NOT NULL,
            date VARCHAR(256) NOT NULL
        );
        """
    )


def flush_vertica(cursor):
    cursor.execute(
        """
            DROP TABLE IF EXISTS test;
            """
    )
