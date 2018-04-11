import codecs
import json

objects = []


def read_json():
    try:
        data_json = codecs.open('insta_geo_new.json', 'r', 'utf-8')
    except Exception as e:
        print(u'Error has occurred')
        print('Error: ', e)
    else:
        with data_json:
            d = json.load(data_json)
            for item in d:
                record = {}
                record['age'] = item['age']
                record['sex'] = item['sex']
                record['tag'] = item['tag']
                record['place'] = item['place']
                record['latitude'] = item['latitude']
                record['longitude'] = item['longitude']
                objects.append(record)