import re 
from textblob import TextBlob 
from textblob.sentiments import NaiveBayesAnalyzer

from flask import Flask, render_template , redirect, url_for, request
import pandas as pd
import scaping




def clean_tweet( tweet): 

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 
         
def get_tweet_sentiment(tweet): 
        
        # analysis = TextBlob(clean_tweet(tweet), analyzer=NaiveBayesAnalyzer()) 

        # if analysis.sentiment.classification == "pos": 
        #     return 'positive'
        # elif analysis.sentiment.classification == "neg": 
        #     return 'negative'

        analysis = TextBlob(clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return "positive"
        elif analysis.sentiment.polarity == 0:
            return "neutral"
        else:
            return "negative"


def get_tweets(query, count=5): 
        
        count = int(count)
        tweets = []
        fetched_tweets = scaping.get_tweets(query,count)
        count_P=0
        count_N=0    
        for tweet in fetched_tweets['tweets']: 
                
            parsed_tweet = {} 
            parsed_tweet['text']=clean_tweet(tweet['text'])
            parsed_tweet['sentiment'] = get_tweet_sentiment(tweet['text']) 
            if(parsed_tweet['sentiment']=="positive"):
                count_P+=1
            elif(parsed_tweet['sentiment']=="negative"):
                count_N+=1
            tweets.append(parsed_tweet) 
        overall="Positive" if count_P>count_N else "Negative"
        return tweets,overall


app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def home():
  return render_template("index.html")

# ******Phrase level sentiment analysis
@app.route("/predict", methods=['POST','GET'])
def pred():
	if request.method=='POST':
            query=request.form['query']
            count=request.form['num']
            fetched_tweets,overall = get_tweets(query, count) 
            return render_template('result.html', result=fetched_tweets ,overall_r=overall)


@app.route("/predict1", methods=['POST','GET'])
def pred1():
	if request.method=='POST':
            text = request.form['txt']
            blob = TextBlob(text)
            if blob.sentiment.polarity > 0:
                text_sentiment = "Positive"
            elif blob.sentiment.polarity == 0:
                text_sentiment = "neutral"
            else:
                text_sentiment = "negative"
            return render_template('result1.html',msg=text, result=text_sentiment)


if __name__ == '__main__':
    app.debug=True
    app.run(host='localhost', port=5000)