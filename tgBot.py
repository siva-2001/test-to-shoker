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

def get_posts(domain):
    #   ----------------------------------------------------------------------------------------------------------------
    #   Возвращает последние посты из VK группы, прерывает выполнение в если
    #   ответа нет больше определённого в config.TIMEOUT времени
    #   ----------------------------------------------------------------------------------------------------------------
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
        video_group = list()

        if 'attachments' not in post.keys():
            bot.send_message(config.TG_CHANNEL, text)
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
                    pass
                    video_player_url = get_video_player_url(
                        attach['video']['owner_id'],
                        attach['video']['id'],
                        attach['video']['access_key']
                    )
                    bot.send_message(channel, video_player_url,)

                elif attach['type'] == 'doc':
                    document_url = urllib.request.urlopen(''.join(attach['doc']['url'].split('\\')))
                    doc_group.append(document_url)
                    bot.send_document(chat_id=channel,document=document_url, visible_file_name=attach['doc']['title'])
                    # Обработка слишком большого файла

            bot.send_media_group(channel, photo_group)
        time.sleep(1)
    return

def check_new_posts(club_domain, channel):
    posts = get_posts(club_domain)
    try:
        with open('VK_club_last_posts_id/'+str(club_domain)+'.txt', 'rt') as file:
            last_posts_id = [int(lpid) for lpid in file.read().split(',')]
        if posts is not None:
            posts_to_sending = []
            for post in posts:
                if post['id'] not in last_posts_id:
                    posts_to_sending.append(post)
                    last_posts_id.append(post['id'])
            with open('VK_club_last_posts_id/'+str(club_domain)+'.txt', 'wt') as file:
                last_posts_id.sort(reverse=True)
                file.write(str(last_posts_id[:config.COUNT_OF_POSTS])[1:-1])
            posts_to_sending.reverse()
            send_new_posts(posts_to_sending, channel)
        return

    except FileNotFoundError as ex:
        logging.error(f'File with last post id for {str(club_domain).upper()} club not exitst: skip iteration, file will be created')
        posts_id = list()
        for post in posts:
            posts_id.append(post['id'])
        with open('VK_club_last_posts_id/'+str(club_domain)+'.txt', 'wt') as file:
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







send_new_posts(get_posts("testclubforinterview"),'@testChannelForMyIBot')



#check_new_posts(config.DOMAIN)
#send_new_posts(get_posts())
#get_video_player_url(258450864, 456239554, '55046c56ad3a5f8f1b')
#get_video_url(get_video_player_url(258450864, 456239554, '55046c56ad3a5f8f1b'))



















