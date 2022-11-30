from kafka import KafkaProducer

print('sending')
producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
future = producer.send('test0', b'hello3')
result = future.get(timeout = 60)
print('sent with ' + str(result))
