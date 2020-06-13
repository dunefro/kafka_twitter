import yaml
from elasticsearch import Elasticsearch
from kafka import KafkaConsumer

with open('creds.yaml') as f:
    creds = yaml.load(f,Loader=yaml.FullLoader)

elasticsearch_url = creds['elasticsearch_url']
elasticsearch_client = Elasticsearch(hosts=elasticsearch_url)
# To test the cluster is working or not
# print(elasticsearch_client.info())

def _group_name(topic):
    return '_'.join([topic,'group'])

def _get_message_id(headers):
    return headers[0][1].decode() # to get the tweet id back in string

def _get_message_body(message):
    return dict(key=message.key,value=message.value,partition=message.partition,offset=message.offset)

def _consume_tweet(topic):
  try:
    consumer = KafkaConsumer(topic,group_id=_group_name(topic),bootstrap_servers=['localhost:9092'],auto_offset_reset='earliest',
                            key_deserializer = lambda a: a.decode(), value_deserializer = lambda a: a.decode())
    # consumer.seek_to_beginning()
    for message in consumer:
        elasticsearch_client.index(index=message.topic,body=_get_message_body(message),id=_get_message_id(message.headers))
        print('Message is successfully put to {} index for partition {} and offset {}'.format(message.topic,message.partition,message.offset))
        # print ('%s:%d:%d: key=%s value=%s headers=%s' % (message.topic, message.partition, message.offset, message.key, message.value,message.headers))
  except KeyboardInterrupt:
      print('Gracefully terminating the consumer')
    
_consume_tweet('trump')
