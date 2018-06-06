import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

class MyListener(StreamListener):
    '''
    This class provides functions that retrieves a data stream of tweets
    for the specified keyword. 
    '''
    def on_data(self, data):
        try:
            # Change name of file as needed
            with open('royal.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
    
# This is the hashtag you are searching for - change as needed
l = ['#royal']
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=l)
