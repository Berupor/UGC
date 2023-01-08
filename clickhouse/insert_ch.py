from clickhouse_driver import Client

client = Client(host='localhost')

client.execute("INSERT INTO default.entry_events VALUES (1994-06-15, 'a1sd');")
