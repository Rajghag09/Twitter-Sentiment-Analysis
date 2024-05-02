from ntscraper import Nitter

def get_tweets(user, count):
    scrapper = Nitter()
    tweets = scrapper.get_tweets(user, mode='user', number=count)
    return tweets

#get_tweets("imVkohli",10)