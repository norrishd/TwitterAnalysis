# TwitterAnalysis
David Norrish Nov-Dec 2017  

Work still very much in progress! Please check back in a couple of weeks for a far more complete thing.

Python scripts for scraping Twitter and carrying out network and sentiment analysis.
Uses the Python Twitter Tools package and Twitter API - https://pypi.python.org/pypi/twitter

## Getting Tweet data
Two options are provided for obtaining Tweet data:
  - The streaming API
  - The search API

Several example files of tweet data are provided as well.

### Optional parameters
These are listed at:
[https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators]

- result_type: recent, popular or mixed (default)
- lang: takes any ISO 639-1 code
- geocode: tweets by users located within a given radius of the given latitude/longitude. The location is preferentially taking from the Geotagging API, but will fall back to their Twitter profile
  -  "latitude,longitude,radius", where radius units must be specified as either "mi" (miles) or "km" (kilometers)
  - e.g. '37.781157 -122.398720 1mi'
- count: up to 100, default = 15
- until: tweets created before a given date.
  - format as YYYY-MM-DD. Keep in mind that the search index has a 7-day limit
  - e.g. '2015-07-19'
- since_id: Returns results with an ID greater than (that is, more recent than) the specified ID
  - e.g. 12345
- max_id: Returns results with an ID less than (that is, older than) or equal to the specified ID
- include_entities: entities node will not be included when set to false


## Network analysis


## Sentiment analysis
