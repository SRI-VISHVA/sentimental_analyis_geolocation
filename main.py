import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import re
from TWLocation import tweetlocation
import numpy as np
import matplotlib.pyplot as plt
import sys

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'RX1TfloBW5z32QGbWalCI8HXE'
        consumer_secret = 'izfNCz9LMwHVVWTtqIWwtN3PQHpdFySPV802sHKjLeypxHSRW6'
        access_token = '1198600156523847681-Foy5c01lD7Hwnt3WTteiuo6iqmLISA'
        access_token_secret = 'o3eX3XO1KOUpx2qniMcKpBzz0d5v5qlHQG5Qqnvyc4Pvi'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                tweet_str = str(tweet)
                parsed_tweet = {}
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def graphing(objects, percentages):
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, percentages, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Percent')
    plt.title('Emotions')
    plt.show()


def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    person = input("Enter the User Name or Trend:\t")
    tweets = api.get_tweets(query=person, count=200)
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    postive_tweet_percentage = 100 * len(ptweets) / len(tweets)
    print("Positive tweets percentage: {} %".format(postive_tweet_percentage))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    negative_tweet_percent = 100 * len(ntweets) / len(tweets)
    print("Negative tweets percentage: {} %".format(negative_tweet_percent))
    # picking neutral tweets from tweets
    nutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    # percentage of neutral tweets
    neutral_tweet_percent = 100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)
    print("Neutral tweets percentage: {} % \
          ".format(neutral_tweet_percent))

    # printing first 10 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 10 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

    # printing first 10 neutral tweets
    print("\n\nNeutral tweets:")
    for tweet in nutweets[:10]:
        print(tweet['text'])

    objects = ('Positve', 'Negative', 'Neutral')
    percentage = [postive_tweet_percentage, negative_tweet_percent, neutral_tweet_percent]

    graphing(objects, percentage)

    cal_tweet_location = input("Do yo want to know the tweet the Person is attending [y/n] :\t")
    if cal_tweet_location == 'y':
        tweetlocation()
    else:
        print('Thank You for using our service')
        sys.exit(0)


if __name__ == "__main__":
    # calling main function
    main()
