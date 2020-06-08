import tweepy
from tweepy.auth import OAuthHandler
import yaml
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError
import random
import logging

logging.basicConfig(level=logging.INFO)

# Setting up Twitter developer client
with open('creds.yaml') as f:
    creds = yaml.load(f,Loader=yaml.FullLoader)
consumer_key = creds['consumer_key']
consumer_secret = creds['consumer_secret']
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)


# custom_partitioner to send data to a particular partition
def _custom_partitioner(key_bytes, all_partitions, available_partitions):
    key_string = key_bytes.decode()
    if key_string == 'tweet':
        return all_partitions[0]
    elif key_string == 'retweet':
        return all_partitions[1]
    else:
        return  random.choice(available_partitions)
    
# Callback function when message is produced successfully
def _msg_sucessfully_produced(msg):
    logging.info('Message produced at topic: {} on partition: {} at the offset: {}'.format(msg.topic,msg.partition,msg.offset))

# Callback function when message failed to get produced
def _msg_failed_to_get_produced(msg):
    logging.error('Message failed to produce, Kindly check')


# Setting up Kafka, acks is default set to 1.
producer = KafkaProducer(bootstrap_servers='localhost:9092',key_serializer= lambda key: key.encode(),value_serializer= lambda value: value.encode(),partitioner = _custom_partitioner,retries=5)

# Step to initialize the message so that duplicate msgs are not sent to the topic
prev_msg = ''

# checks whether the tweet is a retweet and sends the appropriate response back.
# 'RT' string in a tweet declares that it is a retweet
def _check_retweet_status(tweet):

    flag = 'tweet'
    full_text = tweet._json['full_text']
    if 'RT' in full_text[0:3]:
        full_text = tweet._json['retweeted_status']['full_text']
        flag = 'retweet'
    
    return flag , full_text

# checks for duplicate message
def _check_previous_msg(text):

    global prev_msg
    if prev_msg == text:
        return False
    else:
        prev_msg = text
        return True

# tweet will be produced to kafka topic here.
# A topic will be having two partitions, one for normal tweets another for retweets
def _produce_tweet_to_kafka(tweet,topic):

    producer_key , text = _check_retweet_status(tweet)
    if _check_previous_msg(text):
        producer.send(topic,key=producer_key,value=text).add_callback(_msg_sucessfully_produced).add_errback(_msg_failed_to_get_produced)
        return True
    return False

    # Uncomment this if you dont wan't to use key_serializer and value_serializer
    # producer.send(topic,key=producer_key.encode(),value=text.encode())
    # producer.flush()

# flush function is called for flushing any remaining messages
def _call_flush():
    producer.flush()
    producer.close()

query = 'modi'
count = 0
try:
    while True:
        count +=1
        for tweet in tweepy.Cursor(api.search, q=query,tweet_mode='extended').items(1):
            if not _produce_tweet_to_kafka(tweet,query):
                logging.info('Tweet is found to be duplicate. Ignoring the produce to kafka ...')
        time.sleep(5)
        if count > 20:
            _call_flush()
            break

except KeyboardInterrupt:
    logging.warn(' Forceful termiation has been called, Gracefully terminating')
    _call_flush()

