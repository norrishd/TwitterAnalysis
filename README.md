# TwitterAnalysis
David Norrish Nov-Dec 2017  

Scripts for calling the Twitter API to retrieve relevant tweets, then carry out
network, sentiment and NLP analysis.

1. Retrieve some tweet data using twitter_search.py
2. Network analysis with network_analysis.py

Uses the Python Twitter Tools package and Twitter API:
https://pypi.python.org/pypi/twitter

## Getting Tweet data
twitter_search.py takes a search query, optional additional arguments, and
retrieves relevant tweets using the Twitter Search API. Note the API
[rate limits](https://developer.twitter.com/en/docs/basics/rate-limits)
and search [query protocols](https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators).

Optional arguments include:
- count: # of tweets to retrieve (default = 15, max 100 per API call, but
multiple calls will automatically be strung together if needed)
- lang (str): A valid ISO 639-1 code, e.g. 'en'
- result_type: whether to retrieve recent or popular tweets, or a mix (default)
- exact: only retrieve exact phrase matches

More information about Twitter search parameters available [here](https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators)


## Network analysis


## Sentiment analysis
