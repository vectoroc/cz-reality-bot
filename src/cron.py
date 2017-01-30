from parsers import sreality_cz
from parsers import bezrealitky
from db import *
from bot import send_message_all

def cron_task(fetch):
    for item in fetch():
        Flat.update_or_create(item)

def send_updates():
    for item in Chat.select():
        print(item)

if __name__ == '__main__':
    cron_task(sreality_cz.fetch)
    cron_task(bezrealitky.fetch)

    for flat in Flat.allUnsent():
        send_message_all(flat.formatTextMessage())
        flat.markSent()