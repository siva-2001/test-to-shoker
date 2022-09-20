import os
import logging

VK_API_CLUB_URL = f'https://api.vk.com/method/wall.get'
VK_API_VIDEO_URL = 'https://api.vk.com/method/video.get'

TG_CHANNEL = '@testChannelForMyIBot'

#DOMAIN = 'testclubforinterview'
#DOMAIN = '42tomsk'
#   адрес сообщества


COUNT_OF_POSTS = 5
# Количество запрашиваемых постов. При частом постингое должно быть увеличено, либо уменьшен TIMESTEP
# В данной конфигурации ожидается постинг не более 5 записей за 5 минут

TIMESTEP = 5
# Время, через которое происходит новый запроc к VK-api для проверки новых постов, в минутах

TIMEOUT = 8
# Время, по истечении которого при отсутствии ответа запрос к VK-api прерывается, в секундах

VK_API_VERSION = 5.131


#   token was added at 17:00
#   change in release
VK_ACCESS_TOKEN = os.environ.get("VK_ACCESS_TOKEN")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")

#  vk1.a.AVOu-Q7wKxfVU3KTFehMKIa54B3v8n9ZDz15PPrVJcTrPi3mpIptbNhbp1OyutaV-MMMIRF7phnl1v29lIpSHqnGtBJoFvMImpRIJvhSLq__2h2hf7N71YodF1e1w3QhhaeGaN9VI3hD8fOTpszWYYUBCvTqFLM-Se6M6ZecFx7hkKk2gAPKvgYF5pFY3i2H

#
VK_CLUB_TG_CHANNEL = [
    ('testclubforinterview','@testChannelForMyIBot'),
    #(196133541,'@testChannelForMyIBot')

]