# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 14:52:30 2017

@author: User
"""

import json
from twitter import Twitter, OAuth

ACCESS_TOKEN = '383652990-mXwLkiy50TkbwmY1IeOkmXYnQ5pZbtf6PAc2osFd'
ACCESS_SECRET = 'tchtjMAE5pFnA4WVXsFgpD340weOAYqIV6HkcKf045xzw'
CONSUMER_KEY = 'CECKuJNCXNWwLCXAqqvySJEPs'
CONSUMER_SECRET = 'oKz9Cz71yYZivOxdcfXPc9QTS42nXJ2FiVzIR5YFDxGS9S6Kie'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter = Twitter(auth=oauth)

# Get names of places
twitter.search.tweets(q='#nlproc', result_type='recent', lang='en', count=10)

# Get back, e.g.:
'''
{'country': 'Australia',
  'countryCode': 'AU',
  'name': 'Canberra',
  'parentid': 23424748,
  'placeType': {'code': 7, 'name': 'Town'},
  'url': 'http://where.yahooapis.com/v1/place/1100968',
  'woeid': 1100968},
'''

Canberra_trends = twitter.trends.place(_id = 1100968)

print(json.dumps(Canberra_trends, indent = 2))


# Get remaining quota
twitter.application.rate_limit_status()