import logging
import time
import config
import tgBot

if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.INFO,
                            filename='bot_log.log', datefmt='%d.%m.%Y %H:%M:%S')

    while True:
        for vk_tg_pair in config.VK_CLUB_TG_CHANNEL:
            if tgBot.check_new_posts(vk_tg_pair[0], vk_tg_pair[1]) == "Created new file":
                tgBot.check_new_posts(vk_tg_pair[0], vk_tg_pair[1])
        logging.info('[App] Script went to sleep.')
        time.sleep(60 * config.TIMESTEP)
    logging.info('[App] Script exited.\n')