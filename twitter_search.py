"""Twitter tutorial. Reference:

http://socialmedia-class.org/twittertutorial.html
"""

# Optional global variables
sample = False
track_term = "bitch"
lang = "en"
search_by = 'recent'
num = 10

# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    print("Importing simpleJSON instead")
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '383652990-mXwLkiy50TkbwmY1IeOkmXYnQ5pZbtf6PAc2osFd'
ACCESS_SECRET = 'tchtjMAE5pFnA4WVXsFgpD340weOAYqIV6HkcKf045xzw'
CONSUMER_KEY = 'CECKuJNCXNWwLCXAqqvySJEPs'
CONSUMER_SECRET = 'oKz9Cz71yYZivOxdcfXPc9QTS42nXJ2FiVzIR5YFDxGS9S6Kie'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter = Twitter(auth=oauth)

# Get a sample of the public data following through Twitter
tweets = twitter.search.tweets(q = track_term, result_type = search_by, count = num)

# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
for tweet in tweets["statuses"]:
    # Twitter Python Tool wraps the data returned by Twitter 
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
    print(json.dumps(tweet, indent = 2))       

