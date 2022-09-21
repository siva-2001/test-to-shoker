import time
import eventlet
import requests
import logging
import telebot
import config
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib



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
    except:
        logging.warning("Error in get posts from VK")
        return  None
    finally:
        timeout.cancel()

def send_new_posts(posts, channel):
    for post in posts:
        text = post['text']
        photo_group = list()
        doc_group = list()


        if 'geo' in post.keys():
            coords = post['geo']['coordinates'].split(' ')
            latitude, longitude = coords
            bot.send_location(channel, latitude, longitude)

        if 'attachments' not in post.keys():
            bot.send_message(channel, text)
        else:
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
                        bot.send_document(chat_id=channel,document=document_url, visible_file_name=attach['doc']['title'])
                elif attach['type'] == 'poll':
                    question = attach['poll']['question']
                    answer_list = [answer['text'] for answer in attach['poll']['answers']]
                    bot.send_poll(channel, question, answer_list)
            bot.send_media_group(channel, photo_group)

        time.sleep(1)
    return


'''
    check_new_posts проверяет наличие полученных от vk api постов в числе уже размещённых в телеграмм канале,
    и отправляет ещё не опубликованные в ТГ-канал
'''
def check_new_posts(club_domain, channel):
    posts = get_posts(club_domain)
    try:
        with open('VK_club_last_post_id/'+str(club_domain)+'.txt', 'rt') as file:
            # извлекаем id последних опубликованных постов
            last_posts_id = [int(lpid) for lpid in file.read().split(',')]
        if posts is not None:
            posts_to_sending = []
            for post in posts:
                if post['id'] not in last_posts_id:
                    # если пост ещё не был опубликован - сохраняем его данные в post_to_sending
                    posts_to_sending.append(post)
                    last_posts_id.append(post['id'])
            with open('VK_club_last_post_id/'+str(club_domain)+'.txt', 'wt') as file:
                #  перезаписываем файл с id последних постов
                last_posts_id.sort(reverse=True)
                file.write(str(last_posts_id[:config.COUNT_OF_POSTS])[1:-1])
            # Отправляем посты в хронологическом порядке
            posts_to_sending.reverse()
            send_new_posts(posts_to_sending, channel)
        return

    except FileNotFoundError:
        logging.error(f'File with last post id for {str(club_domain).upper()} club not exitst: skip iteration, file will be created')
        posts_id = list()
        for post in posts:
            posts_id.append(post['id'])
        with open('VK_club_last_post_id/'+str(club_domain)+'.txt', 'wt') as file:
            file.write(str(min(posts_id)))
        return "Created new file"
    except ValueError:
        logging.error("file storage is corrupted")
        return
    except Exception as ex:
        logging.error(f"{type(ex).__name__}, {str(ex)}")
        return

def get_video_player_url(owner_id, video_id, video_key):
    #   ----------------------------------------------------------------------------------------------------------------
    #   Возврат URL'a плеера того ресурса, на котором находится файл
    #   ----------------------------------------------------------------------------------------------------------------
    data = requests.get(config.VK_API_VIDEO_URL, params={
        "access_token":config.VK_ACCESS_TOKEN,
        'videos':(str(owner_id)+'_'+str(video_id)+"_"+video_key),
        'owner_id':owner_id,
        'count':config.COUNT_OF_POSTS,
        'v':config.VK_API_VERSION,
    }).json()
    print(data['response']['items'][0]['player'])
    return data['response']['items'][0]['player']

def get_video_url(player_url):
    user_agent = UserAgent()
    header =  {
        'user-agent':user_agent.chrome,
        'sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':"Linux",
    }
    htmlContent = requests.get(player_url).text
    #print(htmlContent)
    soup = BeautifulSoup(htmlContent, 'lxml')
    video_url = soup.find('a', id='movie_player')
    print(video_url)
    return







#send_new_posts(get_posts("testclubforinterview"),'@testChannelForMyIBot')
#check_new_posts(config.DOMAIN)
#send_new_posts(get_posts())
#get_video_player_url(258450864, 456239554, '55046c56ad3a5f8f1b')
#get_video_url(get_video_player_url(258450864, 456239554, '55046c56ad3a5f8f1b'))



















