from kafka import KafkaConsumer


consumer = KafkaConsumer(
    'views',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    group_id='echo_listener',
)

for message in consumer:
    print(message.value)