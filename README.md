# Отправитель уведомлений о проверке работы
Скрипт отправляет уведомления в чат-бот Telegram о проверке работы на сайте devman.org.


# Использование скрипта
Перед использованием необходимо:
 - получить Token для использования API devman.org;
 - зарегистрировать своего бота в Telegram через @BotFather и получить от него **Token**;
 - получить id чата получателя уведомлений через @userinfobot;
 - **Token бота**, **Token API devman.org** и **id** чата перенести в файл .env.
 - Скачать репозиторий https://github.com/ekovalew/bots
 - Установить зависимости ***pip install -r requirements.txt***
 - Запустить код   **python notify_bot.py**

# Деплой скрипта
Пример деплоя для сервера Heroku
- Подключить репозиторий https://github.com/ekovalew/bots во вкладке Deploy;
- Передать **token**, **token_dvmn** и **chat_id** в Settings -> Config Vars
- Подключить бота во вкладке Resources.
 