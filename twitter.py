import os
import json
import urllib
from tweepy import API
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from cj import process

# globals
ckey = os.environ['CKEY']
csecret = os.environ['CSECRET']
atoken = os.environ['ATOKEN']
asecret = os.environ['ASECRET']
userid = os.environ['USERID']

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitter_api = API(auth)

def process_images(images):
    if len(images) == 1:
        images.append('./assets/jordan.png')

    processed = process(images[0], images[1])
    return processed

def download_images(status):
    user = status["user"]["screen_name"]
    status_id = status["id_str"]

    base_path = "./downloads/" + user + '/'
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    output_path = base_path + status_id + '/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    images = status["extended_entities"]["media"]
    image_links = []

    for idx, image in enumerate(images):
        try:
            file_path = output_path + str(idx) + '.jpg'
            urllib.urlretrieve(image["media_url"], file_path)
            image_links.append(file_path)
        except:
            print 'failed to download' + image["media_url"]

    print 'done fetching images!'
    return image_links


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

def reply_with_image(status, image):
    text = "@" + status["user"]["screen_name"]
    twitter_api.update_with_media(image, text, in_reply_to_status_id = status["id"])
    print 'replied with image!'


# stream listener
class listener(StreamListener):

    def on_data(self, data):
        status = json.loads(data)
        if check_valid_status(status):
            images = download_images(status)
            if (len(images) > 0):
                final_image = process_images(images)
                reply_with_image(status, final_image)
            else:
                print 'couldnt download images :('

        return True

    def on_error(self, status):
        print status
        if status == 420:
            print '420 blaze it'
            return False


twitterStream = Stream(auth, listener())
twitterStream.filter(follow=[userid])
