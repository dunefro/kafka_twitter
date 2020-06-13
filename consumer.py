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

def _consume_tweet(topic):
    consumer = KafkaConsumer(topic,group_id=_group_name(topic),bootstrap_servers=['localhost:9092'],auto_offset_reset='earliest',
                            key_deserializer = lambda a: a.decode(), value_deserializer = lambda a: a.decode())
    # consumer.seek_to_beginning()
    for message in consumer:

        print ('%s:%d:%d: key=%s value=%s headers=%s' % (message.topic, message.partition, message.offset, message.key, message.value,message.headers))
    
_consume_tweet('trump')
