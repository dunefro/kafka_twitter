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

# We require only public information so Oauth 2 authentication is used.

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
for tweet in tweepy.Cursor(api.search, q='trump',tweet_mode='extended').items(1):
    print(tweet._json)
    print('--------------------------------------------------------------------------')
    # print(tweet._json['retweeted_status']['entities']['hashtags'].join(' '))
    print('--------------------------------------------------------------------------')
    tweet = {'created_at': 'Mon Jun 15 17:19:01 +0000 2020', 'id': 1272579377440722944, 'id_str': '1272579377440722944', 'full_text': "@CBSSunday As far as Melania using trump's infidelities to re-negotiate her Deal, I believe it's even more salacious. Melania was with trump during the #JeffreyEpsteinChildSexSlave years, and is probably keeping a TON of secrets, like #ghislanemaxwell.\n#trumpepsteinBlackmail", 'truncated': False, 'display_text_range': [11, 275], 'entities': {'hashtags': [{'text': 'JeffreyEpsteinChildSexSlave', 'indices': [152, 180]}, {'text': 'ghislanemaxwell', 'indices': [235, 251]}, {'text': 'trumpepsteinBlackmail', 'indices': [253, 275]}], 'symbols': [], 'user_mentions': [{'screen_name': 'CBSSunday', 'name': 'CBS Sunday Morning 🌞', 'id': 119829799, 'id_str': '119829799', 'indices': [0, 10]}], 'urls': []}, 'metadata': {'iso_language_code': 'en', 'result_type': 'recent'}, 'source': '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', 'in_reply_to_status_id': 1272529525923090434, 'in_reply_to_status_id_str': '1272529525923090434', 'in_reply_to_user_id': 119829799, 'in_reply_to_user_id_str': '119829799', 'in_reply_to_screen_name': 'CBSSunday', 'user': {'id': 61272407, 'id_str': '61272407', 'name': 'PleaseWashYourHands_ThankYou!', 'screen_name': 'taninthesummer', 'location': 'The High Country', 'description': 'Advanced Introvert. Politics! 🚫auto-fbr. I vet. May fbr if u make me laugh or cry, or ur GIFs are cool. No sales! #resist #JoeBiden2020 #Obama #StillWithHer', 'url': None, 'entities': {'description': {'urls': []}}, 'protected': False, 'followers_count': 6060, 'friends_count': 6207, 'listed_count': 6, 'created_at': 'Wed Jul 29 19:19:44 +0000 2009', 'favourites_count': 136095, 'utc_offset': None, 'time_zone': None, 'geo_enabled': False, 'verified': False, 'statuses_count': 201789, 'lang': None, 'contributors_enabled': False, 'is_translator': False, 'is_translation_enabled': False, 'profile_background_color': '000000', 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_tile': False, 'profile_image_url': 'http://pbs.twimg.com/profile_images/1139892772029325313/P7yJtIBg_normal.png', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1139892772029325313/P7yJtIBg_normal.png', 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/61272407/1491585582', 'profile_link_color': '1B95E0', 'profile_sidebar_border_color': '000000', 'profile_sidebar_fill_color': '000000', 'profile_text_color': '000000', 'profile_use_background_image': False, 'has_extended_profile': False, 'default_profile': False, 'default_profile_image': False, 'following': None, 'follow_request_sent': None, 'notifications': None, 'translator_type': 'none'}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 'is_quote_status': False, 'retweet_count': 0, 'favorite_count': 0, 'favorited': False, 'retweeted': False, 'lang': 'en'}
    print(' '.join([hashtags['text'] for hashtags in tweet['entities']['hashtags']]))
    # print(tweet._json['retweeted_status']['full_text'])
    # print(tweet._json['full_text'])   