import twitter
import yaml

with open('creds.yaml') as f:
    creds = yaml.load(f,Loader=yaml.FullLoader)
print(creds)

consumer_key = creds['consumer_key']
consumer_secret = creds['consumer_secret']
access_token = creds['access_token'] 
access_secret_token = creds['access_secret_token']

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_secret_token)

# # print(list(api.GetTrendsCurrent()))
trends = api.GetTrendsWoeid(woeid='2282863')
for trend in trends:
    print(trend)
