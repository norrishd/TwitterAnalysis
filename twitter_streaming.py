"""Twitter tutorial. Reference:

http://socialmedia-class.org/twittertutorial.html
"""

import os
import json

# Optional global variables
sample = False
track_term = "Trump"
lang = "en"


# Import the necessary methods from "twitter" library
from twitter import OAuth, TwitterStream

# Variables that contains the user credentials to access Twitter API 
if 'credentials.txt' in os.listdir():
    creds = open('credentials.txt', 'r')
    ACCESS_TOKEN = creds.readline().strip()
    ACCESS_SECRET = creds.readline().strip()
    CONSUMER_KEY = creds.readline().strip()
    CONSUMER_SECRET = creds.readline().strip()
    creds.close()
else:
    ACCESS_TOKEN = input("Please enter access token:\n")
    ACCESS_SECRET = input("Please enter access token secret:\n")
    CONSUMER_KEY = input("Please enter consumer key:\n")
    CONSUMER_SECRET = input("Please enter consumer key secret:\n")


oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
if sample:
    iterator = twitter_stream.statuses.sample()
else:
    iterator = twitter_stream.statuses.filter(track=track_term, language=lang)

# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
tweet_count = 2
for tweet in iterator:
    tweet_count -= 1
    # Twitter Python Tool wraps the data returned by Twitter 
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
    print(json.dumps(tweet, indent = 2))
           
    if tweet_count <= 0:
        break

# Connect to user stream instead of public stream:
# twitter_userstream = TwitterStream(auth=oauth, domain='userstream.twitter.com')

