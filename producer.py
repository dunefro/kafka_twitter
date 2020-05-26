import tweepy
from tweepy.auth import OAuthHandler
import yaml
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Setting up Twitter developer client
with open('creds.yaml') as f:
    creds = yaml.load(f,Loader=yaml.FullLoader)
consumer_key = creds['consumer_key']
consumer_secret = creds['consumer_secret']
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

# Setting up Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Step to initialize the message so that duplicate msgs are not sent to the topic
prev_msg = ''

# checks whether the tweet is a retweet and sends the appropriate response back
def _check_retweet_status(tweet):

    flag = False
    full_text = tweet._json['full_text']
    if 'RT' in full_text:
        full_text = tweet._json['retweeted_status']['full_text']
        flag = True
    
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
    retweet_status , text = _check_retweet_status(tweet)
    previous_msg_status = _check_previous_msg(text)
    print('{} {}'.format(retweet_status,previous_msg_status))
    producer_key = ''
    if retweet_status and previous_msg_status:
        producer_key = 'retweet'
    elif previous_msg_status:
        producer_key = 'tweet'
    else: 
        return False
    print(text)
    producer.send(topic,key=producer_key.encode(),value=text.encode())
    producer.flush()
    return True

query = 'trump'
count = 0
while True:
    count +=1
    for tweet in tweepy.Cursor(api.search, q=query,tweet_mode='extended').items(1):
        print(tweet._json['full_text'])
        if _produce_tweet_to_kafka(tweet,query):
            print('Push Successful')
        else:
            print('Push Fail')
    time.sleep(5)
    if count > 20:
        break

