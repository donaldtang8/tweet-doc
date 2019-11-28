from selenium import webdriver
from bs4 import BeautifulSoup
from textblob import TextBlob
import json
import re
import pandas as pd
import requests
import sys

class TwitterScraper(object):
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

    def get_sentiment(self, tweet):
        # call TextBlob api to calculate sentiment with cleaned tweet data
        analysis = TextBlob(self.clean_tweet(tweet))
        # if sentiment is greater than 0, it is positive
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        # if sentiment is 0, it is neutral
        elif analysis.sentiment.polarity == 0:
            return 'Neutral'
        # if sentiment is less than 0, it is negative
        else:
            return 'Negative'

    def get_tweets(self, url):
        # create http request to url and get web page content
        all_tweets = []
        response = requests.get(url, timeout=5)
        # if http request code is valid, get web page content
        if response.status_code == 200:
            content = BeautifulSoup(response.text, "html.parser")
            tweets = content.select('#timeline li.stream-item')
            # loop through tweets content and grab tweet id, tweet text, and calculate sentiment
            for tweet in tweets:
                tweet_id = tweet['data-item-id']
                tweet_text = tweet.select('p.tweet-text')[0].get_text()
                tweet_sentiment = self.get_sentiment(tweet_text)
                all_tweets.append({"id": tweet_id, "text": tweet_text, "sentiment": tweet_sentiment}) 
            return all_tweets
        # if http request to url is not valid, exit program
        else:
            print("Invalid twitter handle");
            sys.exit("Invalid twitter handle")

def main(url):
    # create new scraper object
    scraper = TwitterScraper()
    # pass url into object
    tweets = scraper.get_tweets(url)
    # loop through and count amount of positive tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'Positive'] 
    # calculate percentage of positive tweets
    pos = 100*len(ptweets)/len(tweets)
    posCount = len(ptweets);
    # loop through and count amount of negative tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'Negative']
    # calculate percentage of negative tweets
    neg = 100*len(ntweets)/len(tweets)
    negCount = len(ntweets)
    # calculate percentage of neutral tweets
    neut = 100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)
    neutCount = len(tweets) - len(ntweets) - len(ptweets)
    print(json.dumps({"tweets": tweets, "pos": pos, "posCount": posCount, "neg": neg, "negCount": negCount, "neut": neut, "neutCount": neutCount}))


if __name__ == "__main__": 
    # regex to check if url is valid
    """ url = input("Please enter a twitter profile url: ")
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, url):
        main(url)
    else:
        sys.exit("Invalid url") """
    # pass in twitter handle
    # user = input("Please enter a twitter handle: ")
    main("https://twitter.com/" + sys.argv[1])