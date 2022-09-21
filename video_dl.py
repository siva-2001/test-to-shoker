import os
import requests
from tgBot import get_video_player_url
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib


def get_video_url(player_url):
    headers =  {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent':'Chrome / 105.0.0.0',
        #   or   'user-agent':UserAgent().chrome,
        'sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':"Linux",
        'sec-ch-ua-dest':'document',
        'sec-ch-ua-mode':'navigate',
        'sec-ch-ua-site':'none',
        'sec-ch-ua-user':'?1',
        'upgrage-insecure-requests':'1'
    }


    #htmlContent = requests.get(player_url).text
    htmlContent = requests.get(player_url, headers=headers).text

    with open('index.html', 'wt') as file:
        file.write(htmlContent)

    # soup = BeautifulSoup(htmlContent, 'lxml')
    # video_url = soup.find('a', id='movie_player').find(############)
    # print(video_url)
    return

print(get_video_player_url(258450864, 456239554, '55046c56ad3a5f8f1b'))
#   Возвращает ссылку на проигрыватель. Перейдя по ней и глянув инспектор кода виден тег video c src ссылкой на файл
#   "blob:https://vk.com/d90a3be1-f630-4b11-846b-31c03f5af174"
#   И вроде как такой формат можно скачать обходными путями:
#   https://stackoverflow.com/questions/48034696/python-how-to-download-a-blob-url-video
#   Но при переходе по ссылке на плеер в методе get_video_url появляется страница, отличная от той,
#   что видна в браузере (см. index.html)
get_video_url(get_video_player_url(258450864, 456239554, '55046c56ad3a5f8f1b'))
#   судя по всему возвращается версия для мобилки, заголовки эту проблему не фиксят



