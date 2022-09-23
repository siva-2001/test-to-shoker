import os

VK_CLUB_TG_CHANNEL_PAIRS = [
    (189354729,'@testChannelForMyIBot'),
]

# https://oauth.vk.com/authorize?client_id=#&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope-video,photos&response_type=token&v=5.131
VK_ACCESS_TOKEN = os.environ.get("VK_ACCESS_TOKEN")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")


TIMEOUT = 8
    # Время, по истечении которого при отсутствии ответа запрос к VK-api прерывается, в секундах
WITH_ADS = False
    # Постинг рекламных записей
COUNT_OF_POSTS = 10
    # Количество запрашиваемых постов. При частом постингое должно быть увеличено, либо уменьшен TIMESTEP
    # В данной конфигурации ожидается постинг не более 10 записей за 5 минут
    # (на одну меньше в случае наличия закреплённой записи)
TIMESTEP = 5
    # Время, через которое происходит новый запроc к VK-api для проверки новых постов, в минутах
VK_API_VERSION = 5.131
VK_API_CLUB_URL = f'https://api.vk.com/method/wall.get'
VK_API_VIDEO_URL = 'https://api.vk.com/method/video.get'



