import os
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

ckey = os.environ['CKEY']
csecret = os.environ['CSECRET']
atoken = os.environ['ATOKEN']
asecret = os.environ['ASECRET']
userid = os.environ['USERID']

def check_is_mention(status):
    return status.in_reply_to_user_id_str == userid

class listener(StreamListener):

    def on_status(self, status):
        print status
        print "--------------"

        if check_is_mention(status) == True:
            print "is mention"
        else:
            print "nah b"

        return(True)

    def on_error(self, status):
        print status
        if status == 420:
            print '420 blaze it'
            return False


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(follow=[userid])
