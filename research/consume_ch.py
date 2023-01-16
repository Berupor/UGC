from clickhouse_driver import Client

client = Client(host="localhost")

print(client.execute("SELECT * FROM default.test"))
