import requests
import telebot
import os
from dotenv import load_dotenv, find_dotenv
import logging
import time

logger = logging.getLogger(__file__)

def main():
    logging.basicConfig(level=logging.INFO)
    load_dotenv(find_dotenv())
    token = os.environ['TOKEN']
    chat_id = os.environ['CHAT_ID']
    bot = telebot.TeleBot(token);
    token_dvmn = os.environ['TOKEN_DEVMAN']
    header = {'Authorization': token_dvmn}
    param = {}
    logger.info('Бот запустился')

    while True:
        try:
            response = requests.get("https://dvmn.org/api/long_polling/", headers=header, params=param)
            response.raise_for_status()
            review = response.json()
            status = review['status']
            if status == 'timeout':
                timestamp = review['timestamp_to_request']
                param = {'timestamp': timestamp}
            else:
                timestamp = review['last_attempt_timestamp']
                param = {'timestamp': timestamp}
                new_attempt = review['new_attempts'][0]
                lesson = new_attempt['lesson_title']
                url_base = 'https://dvmn.org'
                slug = new_attempt['lesson_url']
                url = f'{url_base}{slug}'
                result = new_attempt['is_negative']
                if result:
                    bot.send_message(chat_id=chat_id,
                                     text=f"Преподаватель проверил работу [{lesson}]({url})!\n К сожалению, в работе нашлись ошибки",
                                     parse_mode='Markdown')
                else:
                    bot.send_message(chat_id=chat_id,
                                     text=f"Преподаватель проверил работу [{lesson}]({url})!\n Преподавателю все понравилось, можно приступать к следующему уроку",
                                     parse_mode='Markdown')
        except requests.exceptions.HTTPError:
            logger.exception('Ошибка')
            time.sleep(5)
            continue
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            logger.exception('Ошибка')
            time.sleep(5)
            continue

if __name__ == '__main__':
    main()
