import os

VK_API_CLUB_URL = f'https://api.vk.com/method/wall.get'
VK_API_VIDEO_URL = 'https://api.vk.com/method/video.get'

TG_CHANNEL = '@testChannelForMyIBot'

WITH_ADS = False

COUNT_OF_POSTS = 10
# Количество запрашиваемых постов. При частом постингое должно быть увеличено, либо уменьшен TIMESTEP
# В данной конфигурации ожидается постинг не более 10 записей за 5 минут
# (на одну меньше в случае наличия закреплённой записи)

TIMESTEP = 5
# Время, через которое происходит новый запроc к VK-api для проверки новых постов, в минутах

TIMEOUT = 8
# Время, по истечении которого при отсутствии ответа запрос к VK-api прерывается, в секундах

VK_API_VERSION = 5.131



VK_ACCESS_TOKEN = os.environ.get("VK_ACCESS_TOKEN")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")

#
VK_CLUB_TG_CHANNEL_PAIRS = [
    #('aasdfanno','@testChannelForMyIBot'),
    ('42tomsk','@testChannelForMyIBot'),
]
