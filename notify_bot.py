import requests
import telebot
import os
from dotenv import load_dotenv, find_dotenv
import logging
import time

logger = logging.getLogger(__file__)


def main():
    logging.basicConfig(filename="sample.log", level=logging.INFO)
    load_dotenv(find_dotenv())
    TOKEN = os.getenv("TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    bot = telebot.TeleBot(TOKEN);
    TOKEN_DVMN = os.getenv("TOKEN_DEVMAN")
    header = {'Authorization': TOKEN_DVMN}
    param = {}

    while True:
        try:
            response = requests.get("https://dvmn.org/api/long_polling/", headers=header, params=param)
            response.raise_for_status()
            response_dec = response.json()
            status = response_dec['status']
            if status == 'timeout':
                timestamp = response_dec['timestamp_to_request']
                param = {'timestamp': timestamp}
            else:
                timestamp = response_dec['last_attempt_timestamp']
                param = {'timestamp': timestamp}
                new_attempt = response_dec['new_attempts'][0]
                lesson = new_attempt['lesson_title']
                url_base = 'https://dvmn.org'
                slug = new_attempt['lesson_url']
                url = f'{url_base}{slug}'
                result = new_attempt['is_negative']
                if result:
                    bot.send_message(chat_id=CHAT_ID,
                                     text=f"Преподаватель проверил работу [{lesson}]({url})!\n К сожалению, в работе нашлись ошибки",
                                     parse_mode='Markdown')
                else:
                    bot.send_message(chat_id=CHAT_ID,
                                     text=f"Преподаватель проверил работу [{lesson}]({url})!\n Преподавателю все понравилось, можно приступать к следующему уроку",
                                     parse_mode='Markdown')
        except requests.exceptions.HTTPError:
            logger.exception('Ошибка')
            break
        except requests.exceptions.ReadTimeout:
            logger.exception('Ошибка')
            time.sleep(2)
            continue


if __name__ == '__main__':
    main()
