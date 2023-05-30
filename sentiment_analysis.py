import pickle
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import re
import tweepy
import os
from dotenv import load_dotenv

model = pickle.load(open('final_model.sav', 'rb'))

STOPWORDS = stopwords.words('english')

def text_cleaner(text, remove_stopwords=True):
    temp = BeautifulSoup(text, 'lxml').get_text() # removes html encoding
    temp.replace("'", "") # avoids removing contractions
    temp = temp.lower() # lowercase
    temp = re.sub(r'@[A-Za-z0-9_]+', '', temp) # removes mentions
    temp = re.sub(r'https?://\S+', '', temp) # removes urls (http/https)
    temp = re.sub(r'www.\S+', '', temp) # removes urls (www.)
    temp = re.sub(r'[&,.]', ' ', temp) # removes all non letters
    temp = re.sub(r'[^a-z\s]+', '', temp)
    # tokenizes and removes stopwords
    temp = temp.split()
    if remove_stopwords: temp = [w for w in temp if w not in STOPWORDS]
    cleaned = " ".join(word for word in temp)
    cleaned = cleaned.strip()
    return cleaned


load_dotenv()
bearer_token = os.getenv('BEARER_TOKEN')
client = tweepy.Client(bearer_token)

def sentiment_analyzer(query):
    filter_retweet = ' -is:retweet'
    filter_mentions = ' -has:mentions'
    filter_replies = ' -is:reply'
    filter_english = ' lang:en'
    
    tweets = client.search_recent_tweets(query=query+filter_retweet+filter_english, max_results=100)
    
    clean_tweets = []
    for tweet in tweets.data:
        clean_tweets.append(text_cleaner(tweet.text))

    predicted_sentiments = model.predict(clean_tweets)
    positive_tweets = []
    negative_tweets = []
    for i, sentiment in enumerate(predicted_sentiments):
        if len(positive_tweets) >= 5 and len(negative_tweets) >= 5: break

        tweet_id = tweets.data[i].id
        embedded_tweet_code = f'<blockquote class="twitter-tweet"><a href="https://twitter.com/x/status/{tweet_id}"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
        if sentiment > 0 and len(positive_tweets) < 5: positive_tweets.append(embedded_tweet_code)
        elif sentiment == 0 and len(negative_tweets) < 5: negative_tweets.append(embedded_tweet_code)
    # for i, clean_tweet in enumerate(clean_tweets):
    #     if predicted_sentiments[i] == 4: 
    #         print(tweets.data[i])
    #         print(clean_tweet)
    return round((sum(predicted_sentiments)/len(predicted_sentiments))*25, 1), positive_tweets, negative_tweets

