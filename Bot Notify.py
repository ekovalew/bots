import requests
import telebot
import os
from dotenv import load_dotenv, find_dotenv
import logging
import time

logging.basicConfig(filename="sample.log", level=logging.INFO)

load_dotenv(find_dotenv())
token = os.getenv("TOKEN")
chat_id = os.getenv("CHAT_ID")
bot = telebot.TeleBot(token);
token_dm = os.getenv("TOKEN_DEVMAN")

header = {'Authorization': token_dm}


def main():
    param = {}
    while True:
        response = requests.get("https://dvmn.org/api/long_polling/", headers=header, params=param)
        respJSON = response.json()
        decoded_response = respJSON
        try:
            response.raise_for_status()
            if 'error' in decoded_response:
                raise requests.exceptions.HTTPError(decoded_response['error'])
            status = respJSON['status']
            if status == 'timeout':
                timestamp = respJSON['timestamp_to_request']
                param = {'timestamp': timestamp}
            else:
                timestamp = respJSON['last_attempt_timestamp']
                param = {'timestamp': timestamp}
                new_attempt = respJSON['new_attempts'][0]
                lesson = new_attempt['lesson_title']
                url = 'https://dvmn.org' + new_attempt['lesson_url']
                result = new_attempt['is_negative']
                if result:
                    bot.send_message(chat_id=chat_id,
                                     text=f"Преподаватель проверил работу [{lesson}]({url})!\n К сожалению, в работе нашлись ошибки",
                                     parse_mode='Markdown')
                else:
                    bot.send_message(chat_id=chat_id,
                                     text=f"Преподаватель проверил работу [{lesson}]({url})!\n Преподавателю все понравилось, можно приступать к следующему уроку",
                                     parse_mode='Markdown')
        except Exception as e:
            logging.error(f'{str(e)}')
            break
        except requests.exceptions.ReadTimeout:
            logging.error('ReadTimeout')
            time.sleep(2)
            continue
        except ConnectionError:
            logging.error('ConnectionError')
            time.sleep(2)
            continue

if __name__ == '__main__':
    main()
