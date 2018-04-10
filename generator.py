import json as j
import re
from result_data import ResultData
from GooglePlacesLibPatch import GooglePlaces
from googleplaces import types, lang, ranking
from hashTypes import hashTypes
import difflib


API_KEY = 'AIzaSyCv3hNhb0HDg8KpxLP0JNqxAPUfUpH-0qU'


class Generator:
    def __init__(self, name, kind):
        self.source_file = name
        self.source_json = {}
        self.target_file = re.sub(r'(.*?)(?=\..*)', r'\1_new', name)
        self.target = None
        self.kind = kind

    @staticmethod
    def __query__(longitude, latitude, tag, hashtags, pages_count=3):

        object_name = ''
        print_types = lambda x: print("Chosen place types", object_item.types)

        #object PLACES NEAR
        google = GooglePlaces(API_KEY)
        query_result = google.nearby_search(
                    lat_lng={'lat': latitude, 'lng': longitude},
                    radius=1000,
                    language=lang.RUSSIAN,
                    type=types.AC_TYPE_ESTABLISHMENT,
                    types=types.AC_TYPE_ESTABLISHMENT,
                    rankby=ranking.DISTANCE
                )
        pages = 0
        object_item = None

        while pages < pages_count and query_result.has_next_page_token:
            print("Page N-", pages)
            # request
            if pages != 0:
                query_result = google.nearby_search(
                    pagetoken=query_result.next_page_token
                )
            # request process
            print("Places found: ", len(query_result.places))
            print("Name of places: ", [place.name for place in query_result.places])
            print("_")
            for item in query_result.places:
                # search item types with chosen tag
                if check_type_tags(item, hashTypes.get(tag, 'другое'), True):
                    object_item = item
                # search item time in hashtags
                if check_type_tags(item, hashtags, True):
                    object_item = item
                # search item name in hashtags
                elif check_type_tags(item, hashtags, False):
                    object_item = item
                if object_item:
                    print_types(item)
                    return item.name
            pages += 1

        # choosing the nearest establishment
        if object_name == '':
            for item in query_result.places:
                if 'sublocality' not in item.types and 'locality' not in item.types or 'establishment' in item.types:
                    object_item = item
            else:
                # if don't find anything after loop then Other
                if object_name == '':
                    object_name = 'Другое'
        if object_item:
            object_name = object_item.name
            print("Nearest place types", object_item.types)

        return object_name

    def process(self, count):
        self.__open__()
        self.target = ResultData()
        steps = min(len(self.source_json), count)
        for i in range(steps):
            print("\nstep: ", i+1, "\\", steps)
            record = self.source_json[i]
            try:
                record['hashtag'] = j.loads(record['hashtag'])
                place = self.__query__(record['longitude'], record['latitude'], record['tag'], record['hashtag'])
                record['place'] = place
                print("place: ", record['place'])
                print("original hash tag: ", record["hashtag"])
                print("tag: ", record["tag"])
                print("long and lat", record['latitude'], record['longitude'])
            except Exception as e:
                print("Got error on step: ", i + 1)
                print("Error: ", str(e))
            finally:
                self.target.add_record(record)

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
                sq = difflib.SequenceMatcher(None, item_type, arr_item)
                if sq.ratio() > 0.6 or find_word_in(item_type, arr_item):
                    return True
        else:
            sq = difflib.SequenceMatcher(None, item.name, arr_item)
            if sq.ratio() > 0.8:
                return True
    return False


def find_word_in(a, b):
    if len(a) < len(b):
        a, b = b, a
    return a in b
