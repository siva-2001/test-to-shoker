import time
import eventlet
import requests
import logging
import telebot
import config
import urllib
import dbm



bot = telebot.TeleBot(config.TG_BOT_TOKEN)

'''
    get_posts() озвращает последние посты из VK группы, прерывает выполнение в если
    ответа нет больше определённого в config.TIMEOUT времени
'''
def get_posts(domain):
    timeout = eventlet.Timeout(config.TIMEOUT)
    try:
        params = {
            'count': config.COUNT_OF_POSTS,
            'access_token': config.VK_ACCESS_TOKEN,
            'v': config.VK_API_VERSION
        }
        if type(domain) == str:
            params['domain'] = domain
        elif type(domain) == int:
            params['owner_id'] = str(-domain)
        data_str = requests.get(config.VK_API_CLUB_URL, params=params)
        return data_str.json()['response']['items']
    except eventlet.timeout.Timeout:
        logging.warning("Got Timeout while retrieving vk JSON data")
        return None
    except Exception as ex:
        logging.warning(f"Error in get posts from VK: {ex}")
        return  None
    finally:
        timeout.cancel()


'''
    send_new_posts() в каждом  полученном посте обрабатывает текст поста и всевозможные прикреплённые файлы,
    отправляет их в тг-канал. Фотографии группируются, для остальных типов такая возможность не поддерживается.
'''
def send_new_posts(posts, channel):
    for iter, post in enumerate(posts):
        text = post['text']
        photo_group = list()

        if 'geo' in post.keys():
            coords = post['geo']['coordinates'].split(' ')
            latitude, longitude = coords
            bot.send_location(channel, latitude, longitude)

        if 'attachments' in post.keys():
            for number, attach in enumerate(post['attachments']):
                if number > 10:
                    break
                if number != 0:
                    # Для корректного отображения текста при множестве файлов он должен быть прикреплён только к первому
                    text = None
                if attach['type'] == 'photo':
                    photo_group.append(telebot.types.InputMediaPhoto(attach['photo']['sizes'][-1]['url'], text))
                elif attach['type'] == 'video':
                    video_player_url = get_video_player_url(
                        attach['video']['owner_id'],
                        attach['video']['id'],
                        attach['video']['access_key']
                    )
                    bot.send_message(channel, attach['video']['title'] + '\n\n' + video_player_url)
                elif attach['type'] == 'doc':
                    if attach['doc']['ext'] == 'gif':
                        bot.send_video(channel, attach["doc"]['url'])
                    else:
                        document_url = urllib.request.urlopen(''.join(attach['doc']['url'].split('\\')))
                        bot.send_document(chat_id=channel, document=document_url,
                                          visible_file_name=attach['doc']['title'], caption=text)
                elif attach['type'] == 'poll':
                    question = attach['poll']['question']
                    answer_list = [answer['text'] for answer in attach['poll']['answers']]
                    bot.send_poll(channel, question, answer_list)
            if len(photo_group) != 0:
                bot.send_media_group(channel, photo_group)
        else:
            bot.send_message(channel, text)
    return


'''
    check_new_posts проверяет наличие полученных от vk api постов в числе уже размещённых в телеграмм канале,
    и отправляет ещё не опубликованные в ТГ-канал
'''
def check_new_posts(club_domain, channel):
    posts = get_posts(club_domain)
    try:
        with dbm.open('VK_club_last_post_id', 'c') as storage:
            # извлекаем id последних опубликованных постов
            last_posts_id = [int(lpid) for lpid in str(storage[club_domain])[2:-1].split(', ')]
        if posts is not None:
            posts_to_sending = []
            for post in posts:
                if post['id'] not in last_posts_id:
                    # если пост ещё не был опубликован - сохраняем его данные в post_to_sending
                    posts_to_sending.append(post)
                    last_posts_id.append(post['id'])
            with dbm.open('VK_club_last_post_id', 'c') as storage:
                #  перезаписываем файл с id последних постов
                last_posts_id.sort(reverse=True)
                storage[club_domain] = str(last_posts_id[:config.COUNT_OF_POSTS])[1:-1]
            # Отправляем посты в хронологическом порядке
            posts_to_sending.reverse()
            send_new_posts(posts_to_sending, channel)
        return
    except ValueError:
        logging.error("file storage is corrupted")
        return
    except KeyError:
        with dbm.open('VK_club_last_post_id', 'c') as storage:
            storage[club_domain] = '0'
        return "Created new file"
    except Exception as ex:
        logging.error(f"{type(ex).__name__}, {str(ex)}, {ex}")
        return

"""
        Возврат URL'a плеера того ресурса, на котором находится файл
"""
def get_video_player_url(owner_id, video_id, video_key):
    data = requests.get(config.VK_API_VIDEO_URL, params={
        "access_token":config.VK_ACCESS_TOKEN,
        'videos':(str(owner_id)+'_'+str(video_id)+"_"+video_key),
        'owner_id':owner_id,
        'count':config.COUNT_OF_POSTS,
        'v':config.VK_API_VERSION,
    }).json()
    return data['response']['items'][0]['player']

