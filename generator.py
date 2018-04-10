import json as j
import re
from result_data import ResultData
from googleplaces import GooglePlaces, types, lang
from hashTypes import hashTypes
API_KEY = 'AIzaSyCv3hNhb0HDg8KpxLP0JNqxAPUfUpH-0qU'


class Generator:
    def __init__(self, name, kind):
        self.source_file = name
        self.source_json = {}
        self.target_file = re.sub(r'(.*?)(?=\..*)', r'\1_new', name)
        self.target = None
        self.kind = kind

    @staticmethod
    def __query__(longitude, latitude, tag, hashtags):

        object_name = ''

        #object PLACES NEAR
        google = GooglePlaces(API_KEY)

        #request
        query_result = google.nearby_search(
            lat_lng={'lat': latitude, 'lng': longitude},
            radius=150,
            language=lang.RUSSIAN
        )

        #request process
        for item in query_result.places:
            #сравнение types с тегами
            if check_type_tags(item, hashTypes.get(tag, 'другое'), True):
                object_name = item.name
            #сравнение types с хештегами
            elif check_type_tags(item, hashtags, True):
                object_name = item.name
            # сравнение types с хештегами
            elif check_type_tags(item, hashtags, False):
                object_name = item.name

        if object_name == '':
            for item in query_result.places:
                if 'locality' not in item.types:
                    object_name = item.name
            else:
                if object_name == '':
                    object_name = 'Другое'
        return object_name

    def process(self, count):
        self.__open__()
        self.target = ResultData()
        steps = min(len(self.source_json), count)
        for i in range(steps):
            print("step: ", i+1, "\\", steps)
            record = self.source_json[i]
            try:
                record['hashtag'] = j.loads(record['hashtag'])
                place = self.__query__(record['longitude'], record['latitude'], record['tag'], record['hashtag'])
                record['place'] = place
                print("place: ", record['place'])
            except BaseException:
                print("Got error on step: ", i + 1)
            finally:
                self.target.add_record(record)
        self.__save__()

    def __open__(self):
        file = open(self.source_file)
        self.source_json = j.load(file)
        self.source_json = self.source_json[2]['data']
        file.close()

    def __save__(self):
        file = open(self.target_file, 'w')
        file.write(j.dumps(self.target.data))
        file.close()

    @staticmethod
    def __converter__(s):
        return s.encode().decode('unicode-escape')


def check_type_tags(item, searched_arr, type_search):
    """
    сравнение types/name с тегами или хештегами записи
    """
    for arr_item in searched_arr:
        if type_search:
            for item_type in item.types:
                if item_type == arr_item:
                    return True
        else:
            for name in item.name:
                if name == arr_item:
                    return True
    return False
