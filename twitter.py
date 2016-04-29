import os
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# globals
ckey = os.environ['CKEY']
csecret = os.environ['CSECRET']
atoken = os.environ['ATOKEN']
asecret = os.environ['ASECRET']
userid = os.environ['USERID']

# only statuses that are replies with photos
def check_valid_status(status):
    if status["in_reply_to_user_id_str"] == userid:
        media = status.get("extended_entities", {}).get("media", None)

        if media is not None:
            valid = False
            for m in media:
                if m["type"] == "photo":
                    valid = True

            return valid
        else:
            return False
    else:
        return False


# stream listener
class listener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        if check_valid_status(data):
            print "is mention"
        else:
            print "nah b"

        return True

    def on_error(self, status):
        print status
        if status == 420:
            print '420 blaze it'
            return False


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(follow=[userid])
