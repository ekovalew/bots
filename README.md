# Отправитель уведомлений о проверке работы
Скрипт отправляет уведомления в чат-бот Telegram о проверке работы на сайте devman.org.

# Установка
`(venv) > pip install notify_bot`

# Использование
Перед использованием необходимо:
 - получить Token для использования API devman.org;
 - зарегистрировать своего бота в Telegram через @BotFather и получить от него **Token**;
 - получить id чата получателя уведомлений через @userinfobot;
 - **Token бота**, **Token API devman.org** и **id** чата перенести в файл .env.
 ```
>>> import notify_bot
>>> notify_bot.main()

```
 