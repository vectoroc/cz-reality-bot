import urllib.request
import urllib.parse
import json

urlBase = 'https://www.bezrealitky.cz'
url1 = 'https://www.bezrealitky.cz/api/search/map?filter=%7B%22order%22:%22time_order_desc%22,%22advertoffertype%22:%22nabidka-pronajem%22,%22estatetype%22:%5B%22byt%22,%22dum%22%5D,%22disposition%22:%5B%222-kk%22,%222-1%22%5D,%22ownership%22:%22%22,%22equipped%22:%22%22,%22priceFrom%22:10000,%22priceTo%22:16000,%22construction%22:%22%22,%22description%22:%22%22,%22surfaceFrom%22:50,%22surfaceTo%22:80,%22balcony%22:%22%22,%22terrace%22:%22%22,%22polygons%22:%5B%5B%7B%22lat%22:50.0857849787494,%22lng%22:14.475173950195312%7D,%7B%22lat%22:50.078074222866334,%22lng%22:14.467277526855469%7D,%7B%22lat%22:50.067277080898286,%22lng%22:14.468650817871094%7D,%7B%22lat%22:50.05669793151598,%22lng%22:14.472427368164062%7D,%7B%22lat%22:50.0458959766676,%22lng%22:14.468650817871094%7D,%7B%22lat%22:50.04148631675135,%22lng%22:14.458351135253906%7D,%7B%22lat%22:50.04038383847727,%22lng%22:14.446678161621094%7D,%7B%22lat%22:50.03963965132947,%22lng%22:14.433245658874512%7D,%7B%22lat%22:50.0462542437422,%22lng%22:14.429769515991211%7D,%7B%22lat%22:50.04537235074825,%22lng%22:14.4175386428833%7D,%7B%22lat%22:50.046695184163,%22lng%22:14.411444664001465%7D,%7B%22lat%22:50.05956291922716,%22lng%22:14.417431585000031%7D,%7B%22lat%22:50.05441098581657,%22lng%22:14.388055801391602%7D,%7B%22lat%22:50.06749745503536,%22lng%22:14.379386901855469%7D,%7B%22lat%22:50.078074222866334,%22lng%22:14.373550415039062%7D,%7B%22lat%22:50.08776754408083,%22lng%22:14.366683959960938%7D,%7B%22lat%22:50.09145710011043,%22lng%22:14.35938835144043%7D,%7B%22lat%22:50.10158815104786,%22lng%22:14.354238510131836%7D,%7B%22lat%22:50.10946026021669,%22lng%22:14.371232986450195%7D,%7B%22lat%22:50.11925730187883,%22lng%22:14.385738372802734%7D,%7B%22lat%22:50.11683574775231,%22lng%22:14.3975830078125%7D,%7B%22lat%22:50.11353343109969,%22lng%22:14.408226013183594%7D,%7B%22lat%22:50.11375359262905,%22lng%22:14.42007064819336%7D,%7B%22lat%22:50.128942293599195,%22lng%22:14.450798034667969%7D,%7B%22lat%22:50.12410004269237,%22lng%22:14.466590881347656%7D,%7B%22lat%22:50.10362511455642,%22lng%22:14.450798034667969%7D,%7B%22lat%22:50.09767914064942,%22lng%22:14.460411071777344%7D,%7B%22lat%22:50.093494494383805,%22lng%22:14.47174072265625%7D,%7B%22lat%22:50.0857849787494,%22lng%22:14.475173950195312%7D,%7B%22lat%22:50.0857849787494,%22lng%22:14.475173950195312%7D,%7B%22lat%22:50.0857849787494,%22lng%22:14.475173950195312%7D,%7B%22lat%22:50.0857849787494,%22lng%22:14.475173950195312%7D,%7B%22lat%22:50.0857849787494,%22lng%22:14.475173950195312%7D,%7B%22lat%22:50.0857849787494,%22lng%22:14.475173950195312%7D,%7B%22lat%22:50.0857849787494,%22lng%22:14.475173950195312%7D,%7B%22lat%22:50.0857849787494,%22lng%22:14.475173950195312%7D,%7B%22lat%22:50.0857849787494,%22lng%22:14.475173950195312%7D%5D%5D%7D&squares=%5B%22%7B%5C%22swlat%5C%22:50,%5C%22swlng%5C%22:12,%5C%22nelat%5C%22:52,%5C%22nelng%5C%22:16%7D%22%5D'
url2 = 'https://www.bezrealitky.cz/api/search/result?ids=%s'


def fetchDetails(ids):
    query = urllib.parse.quote('["' + '","'.join(ids) + '"]')
    req = urllib.request.Request(url2 % query)
    req.add_header('Referer', 'https://www.bezrealitky.cz/vyhledat')
    response = urllib.request.urlopen(req).read()
    data = json.loads(response)
    if not data['status']:
        raise Exception('status is not true')
    return data



def fetchRaw():
    response = urllib.request.urlopen(url1).read()
    data = json.loads(response)
    if not data['status']:
        raise Exception('status is not true')
    return data


def convertData(shortData, fullData):
    for item in shortData:
        fullItem = [i for i in fullData if i['id'] == item['id']][0]
        yield {
            'id': ['id'],
            'hash': 'bezreality:%s' % item['id'],
            'price': item['price'],
            'images': [fullItem['mainImageUrl']],
            'title': " ".join([fullItem['short'], fullItem['address'], fullItem['price']]),
            'text': '',
            'location': {
                'gps': {
                    'lat': item['lat'],
                    'lon': item['lng']
                }
            },
            'url': urlBase + fullItem['url'],
            'data': {
                'short': shortData,
                'full': fullItem,
            }
        }

def fetch():
    shortData = [i for s in fetchRaw()['squares'] for i in s['records']]
    fullData = fetchDetails([i['id'] for i in shortData])
    return convertData(shortData, fullData['records'])
