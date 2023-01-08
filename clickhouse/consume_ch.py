from clickhouse_driver import Client

client = Client(host='localhost')

print(client.execute('SHOW DATABASES'))
print(client.execute('SHOW TABLES FROM default'))
print(client.execute('SELECT * FROM entry_events'))
print(client.execute('SELECT * FROM materialized_view'))
print(client.execute('SELECT * FROM entry_events_queue'))
