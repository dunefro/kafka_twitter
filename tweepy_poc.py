import tweepy
from tweepy.auth import OAuthHandler
import yaml

with open('creds.yaml') as f:
    creds = yaml.load(f,Loader=yaml.FullLoader)

consumer_key = creds['consumer_key']
consumer_secret = creds['consumer_secret']
access_token = creds['access_token'] 
access_token_secret = creds['access_token_secret']

# OAuthHandler is used for user purpose that is why we need to also pass the access keys and tokens.
# AppAuthHandler is used for public data

# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth)
# This will display all the public posts done on the respective creds
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)


# Creating an object with the authentication


api = tweepy.API(auth)
# print(api.search(q="trump",count=1)[0]._json['text'])
# Another way to search for only the messages
for tweet in tweepy.Cursor(api.search, q='trump').items(10):
    print(tweet.text)