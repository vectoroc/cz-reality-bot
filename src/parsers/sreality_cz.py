import urllib.request
import json

url = 'https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_sub_cb=4%7C5&category_type_cb=2&czk_price_summary_order2=10000%7C14000&distance=5&estate_age=8&floor_number=0%7C100&furnished=1%7C3&locality_region_id=10&per_page=20&region=ulice+%C5%BDitn%C3%A1&region_entity_id=122932&region_entity_type=street&tms=1484694988959&usable_area=45%7C10000000000';

def fetchRaw():
    response = urllib.request.urlopen(url).read()
    return json.loads(response)

def convertData(data):
    for estate in data['_embedded']['estates']:
        yield {
            'id': estate['hash_id'],
            'hash': 'sreality:%s' % estate['hash_id'],
            'price': estate['price'],
            'images': [i['href'] for i in estate['_links']['images']],
            'title': '',
            'text': estate['locality'] + ": " + ", ".join(estate['labelsReleased'][0]),
            'location': {
                'gps': estate['gps']
            },
            'url': 'https://www.sreality.cz/detail/pronajem/x/x/x/%d' % estate['hash_id']
        }


def fetch():
    return convertData(fetchRaw())
