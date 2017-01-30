from parsers import sreality_cz
from parsers import bezrealitky
from db import *

def cron_task(fetch):
    for item in fetch():
        Flat.update_or_create(item)


if __name__ == '__main__':
    cron_task(sreality_cz.fetch)
    cron_task(bezrealitky.fetch)

