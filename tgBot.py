import time
import eventlet
import requests
import logging
import telebot
import config
import urllib
from time import sleep



bot = telebot.TeleBot(config.TG_BOT_TOKEN)

def get_posts():
    timeout = eventlet.Timeout(10)
    try:
        data_str = requests.get(config.VK_API_URL)
        return data_str.json()['response']['items']
    except eventlet.timeout.Timeout:
        logging.warning("Got Timeout while ")
    except:
        logging.error("Error in get posts from VK")
    finally:
        timeout.cancel()


def send_new_posts(posts_dictionary):
    for post in posts_dictionary:
        text = post['text']
        media_group = list()

        for number, file in enumerate(post['attachments']):
            if number != 0:
                text = None
            if file['type'] == 'photo':
                media_group.append(telebot.types.InputMediaPhoto(media=file['photo']['sizes'][-1]['url'], caption=text))
            elif file['type'] == 'video':
                pass
            elif file['type'] == 'audio':
                pass
            elif file['type'] == 'doc':
                pass
        bot.send_media_group(config.CHANNEL, media_group)
    return

    #for video - video.get in url api
    # try block

def check_new_posts():



send_new_posts(get_posts())
#send_new_posts()















