import tweepy
import time

auth = tweepy.OAuthHandler('', '')
auth.set_access_token('', '')

api = tweepy.API(auth)
user = api.me()

# get my feed
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)


# set a limit for API calls
def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()
    except tweepy.RateLimitError:
        time.sleep(1000)


# using pagination (Cursor object) to print follower names
for follower in limit_handler(tweepy.Cursor(api.followers).items()):
    print(follower.name)
    if follower.name == 'AndreasK':
        follower.follow()
        break


search_string = 'python'
numberofTweets = 2

for tweet in limit_handler(tweepy.Cursor(api.search, search_string).items(numberofTweets)):
    try:
        tweet.favorite()
        tweet.retweet()
        print('I liked that tweet')
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break