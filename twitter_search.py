"""Call Twitter API to search and retrieve relevant tweets.

David Norrish November 2017, norrish.d@gmail.com

Takes a search query and various other possible parameters, outputs relevant
tweets to a .bz2 file.

Note: Twitter API requires a user access token, secret, consumer key and
consumer secret. These are looked for in a file named "credentials.txt", 
located in the same directory on separate lines with nothing else. See tutorial
located here for how to generate credentials:
https://www.slickremix.com/docs/how-to-get-api-keys-and-tokens-for-twitter/

Script inspired by tutorial at:
http://socialmedia-class.org/twittertutorial.html
"""

import re        # for checking whether file name extension included
import os        # for checking whether credentials.txt file present
from twitter import Twitter, OAuth
import bz2       # for writing to .bz2 file
import io        # for wrapping string output to encode
import json      # for converting Twitter library object to dictionary
import sys       # to determine if invoked from command line or IDE
import argparse

def search_tweets(query, **kwargs):
    """Retrieve tweets according to provided parameters and export to bz2 file.
    
    Only requires a query string; accepts optional arguments as a dictionary:
    - count (int): up to 100, default = 15
    - file (str): filename to write to
    - lang (str): A valid ISO 639-1 code
    - result_type (str): 'recent', 'popular' or 'mixed' (default)
    - exact (bool): only include exact phrase matches
    - until (str): restricts to tweets up til YYYY-MM-DD (e.g. '2017-11-20')
    - since_id (int): min ID value for returned tweets
    - max_id (int): max ID value for returned tweets
    - include_entities (str): include entities node? (default = false)
    """
    # If count specified, extract that, otherwise default to 15
    if 'count' in kwargs:
        extra_to_retrieve = kwargs.pop('count')
    else:
        extra_to_retrieve = 15
        
    # Extract file name to write results to. Add '.txt.bz2' extention if needed
    if 'file' in kwargs:
        filename = './tweets/' + kwargs.pop('file')
        if not re.search('\.txt\.bz2$', filename):
            filename = filename + '.txt.bz2'
    else:
        filename = './tweets/tweets.txt.bz2'
    
    # If exact search specified, enclose in quotation marks (multi-word queries)
    if 'exact' in kwargs:
        exact = kwargs.pop('exact')
        if len(query) > 1 and exact:
            query = '"' + query + '"'

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
    
    # Save tweets to .bz2 file
    output = bz2.BZ2File(filename, 'w')
    tweets_parsed = 0
    max_id = float('inf')
    print('Retrieving tweets for query {}...'.format(query))
    # BZ2 needs strings to be encoded, so use TextWrapper
    with io.TextIOWrapper(output, encoding='utf-8') as wrapper:
        # If retrieving > 100 tweets, will need several API calls
        while extra_to_retrieve > 0:
            if tweets_parsed > 0:
                print('Total tweets parsed: {}'.format(tweets_parsed))
            to_retrieve = min(extra_to_retrieve, 100)
            
            # Retrieve tweets by calling the Twitter search API            
            tweets = twitter.search.tweets(q=query, count=to_retrieve, **kwargs)

            for tweet in tweets['statuses']:
                wrapper.write(json.dumps(tweet))
                wrapper.write('\n')
                # Find the earliest tweet to use as threshold for next batch
                if tweet['id'] < max_id:
                    max_id = tweet['id']
                    kwargs['max_id'] = max_id
                extra_to_retrieve -= 1
                tweets_parsed += 1
            kwargs['max_id'] -= 1    # decrement to avoid including threshold tweet twice
        
    output.close()
    
    # Check API rate limit status
    lim = twitter.application.rate_limit_status()['resources']['search']['/search/tweets']
    print('\nRetrieved {} relevant tweets'.format(tweets_parsed))
    print('Saved to file {}'.format(filename))
    print('\nRemaining API calls for current time period: {} of {}'.format(lim['remaining'], lim['limit']))


# Invoke function if called from console. Note I'm not sure this is robust
if len(sys.argv) > 1:
    parser = argparse.ArgumentParser(description='Scrape tweets for a given query.')
    parser.add_argument('query', help='The search query', type=str, default='happy')
    parser.add_argument('-l', '--lang', help='Restrict retrieved tweets to a given language', type=str)
    parser.add_argument('-r', '--result_type', help='Choose between recent and popular tweets', type=str, choices=['recent', 'popular', 'mixed'])
    parser.add_argument('-c', '--count', help='Number of tweets to retrieve', type=int)
    parser.add_argument('-u', '--until', help='Final date to retrieve tweets until', type=str, metavar='YYYY-MM-DD')
    parser.add_argument('-s', '--since_id', help='Min tweet ID to retrieve', type=int)
    parser.add_argument('-m', '--max_id', help='Max tweet ID to retrieve', type=int)
    parser.add_argument('-i', '--include_entities', help='Whether to include entities node', type=str, choices=['true', 'false'])
    parser.add_argument('-f', '--file', help='File name to write the results to.', type=str)
    parser.add_argument('-e', '--exact', help='Only retrieve exact query matches', action='store_true')
    args = parser.parse_args()
    
    # Convert args to a dictionary
    kwargs = {}
    for key, value in vars(args).items():
        if value != None:
            kwargs[key] = value
    
    search_tweets(**kwargs)
