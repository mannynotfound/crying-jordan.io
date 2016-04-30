import os
import json
import urllib
import time
import tweepy
from cj import process

# globals
ckey = os.environ['CKEY']
csecret = os.environ['CSECRET']
atoken = os.environ['ATOKEN']
asecret = os.environ['ASECRET']
userid = os.environ['USERID']

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitter_api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

def print_break():
    print ''
    print '------------------------'
    print ''

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


# check if tweet has photos
def has_pics(status):
    media = status.get("extended_entities", {}).get("media", False)

    if media:
        valid = False
        for m in media:
            if m["type"] == "photo":
                valid = True

        return valid
    else:
        return False


# only statuses that are replies with photos
def check_mention(status):
    reply = status.get("in_reply_to_user_id_str", False)
    return reply == userid


# only cc's that originate from a photo post
def check_quote(status):
    quote = status.get("quoted_status_id", False)

    if not quote:
        return status
    else:
        return twitter_api.statuses_lookup([quote], include_entities = True)[0]


# check if is mention or a mention with quote
# if quote, use the quoted status as the status going forward
def check_valid_status(status):
    mention = check_mention(status)

    if not mention:
        return False
    else:
        status = check_quote(status)
        return status if has_pics(status) else False


def reply_with_fail(status):
    text = "@" + status["user"]["screen_name"]
    text += ' could not process your image :( '
    text += time.strftime("%Y%m%d-%H%M%S")

    twitter_api.update_status(text, in_reply_to_status_id = status["id"])
    print 'replied with fail! :('


def reply_with_image(status, image):
    text = "@" + status["user"]["screen_name"]
    twitter_api.update_with_media(image, text, in_reply_to_status_id = status["id"])
    print 'replied with image!'


def clean_up(images):
    for image in images:
        print 'removing ' + image
        os.remove(image)

    print 'done cleaning up!'
    print_break()


# stream listener
class listener(tweepy.StreamListener):

    def on_data(self, data):
        status = json.loads(data)
        print status
        print ''
        valid_status = check_valid_status(status)

        if valid_status:
            images = download_images(valid_status)
            print images
            print type(images)
            if (len(images)):
                final_image = process_images(list(images))
                if final_image:
                    reply_with_image(valid_status, final_image)
                    images.append(final_image)
                    clean_up(images)
                else:
                    reply_with_fail(valid_status)
                    clean_up(images)
            else:
                print 'couldnt download images :('
        else:
            print 'ignoring stream event'
            print_break()

        return True

    def on_error(self, status):
        print status
        if status == 420:
            print '420 blaze it'
            return False


twitterStream = tweepy.Stream(auth, listener())
twitterStream.filter(follow=[userid])
