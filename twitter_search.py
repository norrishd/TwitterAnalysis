"""Call Twitter API to search and retrieve relevant tweets.

David Norrish November 2017, norrish.d@gmail.com

Expects a 4-line file named "credentials.txt" in the same directory that
contains the user's access token, acess token secret, consumer key and consumer
key secret on separate lines, with nothing else.



Inspired by tutorial at:
http://socialmedia-class.org/twittertutorial.html
"""

# Import the necessary package to process data in JSON format
from twitter import Twitter, OAuth
import json
import bz2
import os
import argparse
import io

def search_tweets(**kwargs):
    """Retrieve tweets according to provided parameters and export to bz2 file.
    
    Accepts optional arguments:
        q (str): A query string
        lang (str): A valid ISO 639-1 code
        result_type (str): 'recent', 'popular' or 'mixed' (default)
        count (int): up to 100, default = 15
        until (str): Tweets up til YYYY-MM-DD (e.g. '2017-11-20')
        since_id (int): min ID value for returned tweets
        max_id (int): max ID value for returned tweets
        include_entities (str): include entities node? (default = false)
    """
    # If no query provided, use a default query of "happy"    
    if 'q' in kwargs:
        query = kwargs.pop('q')
    else:
        query = 'happy'
    
    # If count specified, extract that, otherwise default to 15
    if 'count' in kwargs:
        extra_to_retrieve = kwargs.pop('count')
    else:
        extra_to_retrieve = 15
        
    # Extract file name to write results to, if defined
    if 'file' in kwargs:
        filename = './tweets/' + kwargs.pop('file')
    else:
        filename = './tweets/tweets.txt.bz2'

    # Read in credentials for OAuth
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
    
    # Initiate the connection to Twitter Streaming API
    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter = Twitter(auth=oauth)
    
    # Save tweets to file, both .txt and .bz2 for now (TODO delete .txt later)
    #scrub = open('tweets.txt', 'w')
    #scrub.close()
    #file_out = open('tweets.txt', 'a')
    output = bz2.BZ2File(filename, 'w')
    max_id = float('inf')
    
    with io.TextIOWrapper(output, encoding='utf-8') as wrapper:
        # Twitter library wraps the data returned by Twitter as a 
        # 'TwitterDictResponse' object. Convert it back to JSON format to save
        indices = []
        tweets_parsed = 0
        while extra_to_retrieve > 0:
            # Retrieve tweets by calling the Twitter search API
            to_retrieve = min(extra_to_retrieve, 100)
            print('Total tweets parsed: {}'.format(tweets_parsed))
            tweets = twitter.search.tweets(q=query, count=to_retrieve, **kwargs)
        
            for tweet in tweets['statuses']:
                wrapper.write(json.dumps(tweet))
                wrapper.write('\n')
                #file_out.write(json.dumps(tweet))
                #file_out.write('\n')
                indices.append(tweet['id'])
                if tweet['id'] < max_id:
                    max_id = tweet['id']
                    kwargs['max_id'] = max_id
                extra_to_retrieve -= 1
                tweets_parsed += 1
            kwargs['max_id'] -= 1    # decrement to avoid including threshold tweet twice
        
    output.close()
    indices.sort()
    #file_out.close()
    
    # Check API rate limit status
    lim = twitter.application.rate_limit_status()['resources']['search']['/search/tweets']
    print('Remaining API search calls in current time period: {} of {}'.format(lim['remaining'], lim['limit']))

parser = argparse.ArgumentParser(description='Scrape tweets for a given search term.')
parser.add_argument('-q', '--q', help='The search term', type=str, default='happy')
parser.add_argument('-l', '--lang', help='Restrict retrieved tweets to a given language', type=str)
parser.add_argument('-r', '--result_type', help='Choose between recent and popular tweets', type=str, choices=['recent', 'popular', 'mixed'])
parser.add_argument('-c', '--count', help='Number of tweets to retrieve', type=int)
parser.add_argument('-u', '--until', help='Final date to retrieve tweets until', type=str, metavar='YYYY-MM-DD')
parser.add_argument('-s', '--since_id', help='Min tweet ID to retrieve', type=int)
parser.add_argument('-m', '--max_id', help='Max tweet ID to retrieve', type=int)
parser.add_argument('-i', '--include_entities', help='Whether to include entities node', type=str, choices=['true', 'false'])
parser.add_argument('-f', '--file', help='File name to write the results to.', type=str)

args = parser.parse_args()
kwargs = {}

for key, value in vars(args).items():
    if value != None:
        kwargs[key] = value

search_tweets(**kwargs)
