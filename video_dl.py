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

