import tweepy
from tweepy.auth import OAuthHandler
import yaml

with open('creds.yaml') as f:
    creds = yaml.load(f,Loader=yaml.FullLoader)

consumer_key = creds['consumer_key']
consumer_secret = creds['consumer_secret']

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth)

# checks whether the tweet is a retweet
def _check_retweet_status(tweet):
    if 'RT' in tweet:
        return True
    return False

# tweet will be produced to kafka topic here.
def _produce_tweet_to_kafka(tweet):
    retweet_status = _check_retweet_status(tweet._json['full_text'][0:3])
    if retweet_status:
        print(tweet._json['retweeted_status']['full_text'])
        # text = tweet._json['retweeted_status']['full_text']
    else:
        print(tweet._json['full_text'])
        #text = tweet._json['full_text']

for tweet in tweepy.Cursor(api.search, q='trump',tweet_mode='extended').items(1):
    _produce_tweet_to_kafka(tweet)