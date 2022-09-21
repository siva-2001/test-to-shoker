import logging
import time
import config
import tgBot

if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.INFO,
                            filename='bot_log.log', datefmt='%d.%m.%Y %H:%M:%S')

    while True:
        for (vk_club, tg_channel) in config.VK_CLUB_TG_CHANNEL:
            if tgBot.check_new_posts(vk_club, tg_channel) == "Created new file":
                tgBot.check_new_posts(vk_club, tg_channel)
        logging.info('[App] Script went to sleep.')
        time.sleep(60 * config.TIMESTEP)
    logging.info('[App] Script exited.\n')