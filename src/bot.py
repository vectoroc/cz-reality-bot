import config
import telebot
import json
from db import *
from parsers import sreality_cz

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


bot = telebot.TeleBot(config.token)

# Обработчик команд '/start' и '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    Chat.register(message.chat)

    # json.dumps(message.chat)
    bot.send_message(message.chat.id, 'Hello. Send me url to sreality or bezrealitky.')

# Обработчик команд '/stop'
@bot.message_handler(commands=['stop'])
def handle_stop(message):
    Chat.stop(message.chat)

@bot.message_handler(commands=['sub'])
def handle_subscribe(message):
    bot.send_message(message.chat.id, 'Hello. Send me url to sreality or bezrealitky.')

@bot.message_handler(commands=['test'])
def handle_subscribe(message):
    print(message.chat)
    for item in sreality_cz.fetch():
        bot.send_message(message.chat.id, item['text'] + "\n" + item['url'])
        # bot.send_message(message.chat.id, "\n".join(item['images']))


def send_message_all(text):
    for chat in Chat.aliveChats():
        bot.send_message(chat.id, text)

# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
#     bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    db.connect()
    # db_create_tables()
    bot.polling(none_stop=True)
    db.close()

