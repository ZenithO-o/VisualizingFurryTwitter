from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import json

def getAuth():
    twitterkey = {}
    with open("Twitterkey.json") as json_file:
        twitterkey = json.load(json_file)

    auth = OAuthHandler(twitterkey["consumer_key"],twitterkey["consumer_secret"])
    auth.set_access_token(twitterkey["access_token"],twitterkey["access_token_secret"])
    return auth


class TwitterClient():
    '''
    Client reader for various Twitter accounts
    '''
    def __init__(self):
        self.auth = getAuth()
        self.twitter_client = API(self.auth,wait_on_rate_limit=True)

    def _get_iter(self, api_call, user):
        iter_vals = list()
        for page in Cursor(api_call, id=user, wait_on_rate_limit=True).pages():
            print(page[:5])
            iter_vals.extend(page)
        return iter_vals

    def get_twitter_client_api(self):
        return self.twitter_client
    
    def get_user(self, user):
        return self.twitter_client.get_user(id = user)

    def get_user_tweets(self, user, num=None):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=user, tweet_mode='extended', wait_on_rate_limit=True).items(num):
            tweets.append(tweet)
        return tweets
    
    def get_user_followers(self, user):
        followers = set()
        followers.update(self._get_iter(self.twitter_client.followers_ids, user))
        return followers
    
    def get_user_friends(self, user):
        friends = set()
        friends.update(self._get_iter(self.twitter_client.friends_ids, user))
        return friends
