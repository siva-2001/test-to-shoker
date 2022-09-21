import os

import youtube_dl
from logging import Logger
import time


def my_hook(d):
    print(d['downloaded_bytes'],"/", d['total_bytes'])
    time.sleep(1)
    os.system('clear')
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

#
ydl_opts = {}
#      'format': 'bestaudio/best',
#      'postprocessors': [{
#          'key': 'FFmpegExtractAudio',
#          'preferredcodec': 'mp4',
#          'preferredquality': '192',
#      }],
#      'logger': Logger(name="video_dl_logger"),
#      'progress_hooks': [my_hook],
# }

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://vk.com/video_ext.php?oid=258450864&id=456239554&hash=c313418e6f213de4&__ref=vk.api&api_hash=1663693201bb82dd077799546986_GE4DSMZVGQ3TEOI'])
