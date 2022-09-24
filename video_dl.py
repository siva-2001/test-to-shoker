import urllib.request
from pytube import YouTube
from selenium import webdriver
from bs4 import BeautifulSoup
import logging
import time

def download_video_from_youtube(url):
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True).desc().first()
    video.download('video_files')

def download_video_from_vk(owner_id, video_id, name):
    try:
        url = f'https://m.vk.com/video{owner_id}_{video_id}'
        with webdriver.Chrome() as chrome:
            chrome.get(url)
            htmlContent = chrome.page_source
        html_soup = BeautifulSoup(htmlContent, 'lxml')
        file_urls = [str(url).split(" ")[1][5:-1] for url in
                     html_soup.find('div', id=f'video{owner_id}_{video_id}').findAll('source', type="video/mp4")]

        max_resolution = 0
        high_quality_video_url = ''
        for url in file_urls:
            resolution_len = 3
            resol_start_pos = url.find('.mp4?extra=') - 4
            if url[resol_start_pos] == '.': resol_start_pos += 1
            else: resolution_len = 4
            if int(url[resol_start_pos : resol_start_pos + resolution_len]) > max_resolution:
                max_resolution = int(url[resol_start_pos : resol_start_pos + resolution_len])
                high_quality_video_url = url
        urllib.request.urlretrieve(high_quality_video_url, 'video_files/' + name)
        return 'video_files/' + name
    except Exception as ex:
        print(f"{type(ex).__name__}, {str(ex)}, {ex}")
        logging.error(f"{type(ex).__name__}, {str(ex)}, {ex}")

#urllib.request.urlretrieve("https://vkvd147.mycdn.me/?srcIp=37.21.186.173&amp;pr=40&amp;expires=1664489994501&amp;srcAg=CHROME&amp;fromCache=1&amp;ms=45.136.21.149&amp;type=1&amp;sig=kQmscuxzfvA&amp;ct=0&amp;urls=45.136.22.137&amp;clientType=14&amp;appId=512000384397&amp;id=2779509492386")
#urllib.request.urlretrieve("https://pvv4.vkuservideo.net/c520131/17/e68MDYxPTMxMjA3/videos/0f5f1a34fb.720.mp4?extra=ImDoeBahJM_sa_YVqARcP5jSdBzAF4UpUtpmx-DAb66enbLNITVCQ_3R7rGkmktvGOx3Gcy65vqmANbLqm0cKV0LJbZ2YDWTZIcWxejAhXYjOz1k8AnoQ_4drHN6rdgEZGAZt5DXt4nX1Poqmw&amp;c_uniq_tag=Nh0DqYoyz7mHsVXwkLTVXAakKy4XpTIDXI5rEEdFBoA", 'video')

