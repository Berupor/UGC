from kafka import KafkaConsumer


consumer = KafkaConsumer(
    'entry-events',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    group_id='echo_listener',
)

for message in consumer:
    print(message.value)