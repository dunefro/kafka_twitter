from kafka import KafkaConsumer

def _consume_tweet(topic):
    consumer = KafkaConsumer(topic,group_id=topic+'-'+'group',bootstrap_servers=['localhost:9092'],auto_offset_reset='earliest')
    for message in consumer:
        print ('%s:%d:%d: key=%s value=%s' % (message.topic, message.partition, message.offset, message.key, message.value))
    
_consume_tweet('modi')