import requests
from pprint import pprint
import telebot

chat_id = '1023420974'
bot = telebot.TeleBot('1642990318:AAHkfnOuwg4fcDJycdbdhJOhKq4qSNWTc34');

header = {'Authorization': 'Token cdcf22419df29b18f8d6f8e77262b923151e01ff'}
param = {}
while True:
    try:
        response = requests.get("https://dvmn.org/api/long_polling/", headers=header, params=param)
        if response.json()['status'] == 'timeout':
            timestamp = response.json()['timestamp_to_request']
            param = {'timestamp': timestamp}
        else:
            param = {}
            lesson = response.json()['new_attempts'][0]['lesson_title']
            url = 'https://dvmn.org' + response.json()['new_attempts'][0]['lesson_url']
            result = response.json()['new_attempts'][0]['is_negative']
            if result is True:
                bot.sendMessage(chat_id, "Преподаватель проверил работу [" + lesson +  "](" + url + ")!\n К сожалению, в работе нашлись ошибки", parse_mode='Markdown')
            else:
                bot.send_message(chat_id=chat_id,
                                 text="Преподаватель проверил работу [" + lesson +  "](" + url + ")!\n Преподавателю все понравилось, можно приступать к следующему уроку", parse_mode='Markdown')
        pprint(response.json())
    except requests.exceptions.ReadTimeout:
        continue
    except ConnectionError:
        continue
